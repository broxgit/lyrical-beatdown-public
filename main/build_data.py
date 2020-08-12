import logging
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from database.sql_alchemy.serializer import create_artist_for_db, create_album_for_db, create_song_for_db
from database.sql_alchemy.declarative import *
from database.sql_alchemy.insert import insert_artist, insert_album, insert_song
from database.sql_alchemy.sa_utils import managedSession, initialize, get_sql_file
from genius.genius_api import *

from genius.models.song_lite import GeniusSongLite
from logger import logger
from music_brainz.get_data import get_artist_albums_from_mb, get_artist_data
from music_brainz.models.album import Album as Mb_Album
from utils.misc_utils import *

ARTISTS = ['Senses Fail', 'The Used', 'Taking Back Sunday', 'Underoath']

LOGGER = logger.setup_logger('root', logging.DEBUG)


def track_has_primary_artist(g_song, artist):
    if not check_for_excluded(g_song.title):
        if g_song.primary_artist:
            if g_song.primary_artist.name:
                primary_artist = g_song.primary_artist.name
                if not compare_strings(artist, primary_artist):
                    return False
    else:
        return False
    return True


def track_has_title(g_song):
    if g_song.title:
        return True

    logger.debug(LOGGER, g_song.lyrics_state)
    return False


def get_artist_from_genius(artist_name):
    artist = search_artist(artist_name)
    if artist:
        return artist
    return None


def get_songs_from_genius(genius_artist_id):
    start = time.time()
    songs = []
    for i in range(1, 100):
        _songs = get_artist_songs(genius_artist_id, i)
        if 'songs' in _songs:
            for s in _songs['songs']:
                g_song = GeniusSongLite().from_dict(s)
                songs.append(g_song)
        if not _songs["next_page"]:
            break

    end = time.time()
    elapsed = end - start
    logger.debug(LOGGER, "Collecting songs completed in {} seconds!".format(elapsed))
    return songs


def check_genius_songs(g_song, valid_songs):
    valid_genius_songs = []
    if track_has_title(g_song):
        clean_title = remove_punc(g_song.title)
        if clean_title in valid_songs:
            if track_has_primary_artist(g_song, artist):
                valid_genius_songs.append(g_song)
        else:
            for vs in valid_songs:
                if compare_strings(vs.title(), clean_title, strip_spaces=True):
                    if track_has_primary_artist(g_song, artist):
                        valid_genius_songs.append(g_song)
                logger.debug(LOGGER, 'Song is not in valid songs: {}'.format(clean_title))
    return None


def build_album_data(session, artistId, album_name, songs, valid_album, artist_name):
    # with managedSession() as session:
    # album = None
    album = Album.find_by_name(session, album_name, artistId)

    if not album:
        album = insert_album(session, create_album_for_db(artistId, valid_album, artist_name))

    if album:
        if album.id:
            for song in songs:
                create_song(session, song, valid_album, artistId, album.id)
        else:
            logger.debug(LOGGER, "Album does not have an id : {}".format(album_name))

    return album


def create_song(session, song, valid_album: Mb_Album, artist_id, album_id):
    if valid_album.tracks:
        for track in valid_album.tracks:
            if compare_strings(song.title, track.title):
                s_song = create_song_for_db(song, artist_id, album_id, track)
                insert_song(session, s_song)
                return

        for track in valid_album.tracks:
            if compare_strings(song.title, track.title, strip_spaces=True):
                s_song = create_song_for_db(song, artist_id, album_id, track)
                insert_song(session, s_song)
                return

    logger.debug(LOGGER, '{} does not have a match in the track list'.format(song.title))
    return None


def thread_songs(songs: List[GeniusSongLite], artistId, artistName):
    with managedSession() as session:
        song_list = []

        for song in songs:
            _song = Song.find_by_name(session, song.title, artistId)
            if not _song:
                _song = search_song(song.title, artistName)
                if _song:
                    song_list.append(_song)

        session.flush()
        session.commit()

        return song_list


def get_valid_album(valid_albums: List[Mb_Album], album_name):
    for va in valid_albums:
        if compare_strings(va.mb_data.title, album_name):
            return va
    logger.error(LOGGER, "SOMETHING HAS GONE TERRIBLY WRONG! (get_valid_album) {}".format(album_name))
    return None


def build_artist_data(artist):
    with managedSession() as session:
        db_artist = Artist.find_by_name(session, artist)

        mb_artist = get_artist_data(artist)

        if not mb_artist:
            return None

        valid_albums = get_artist_albums_from_mb(mb_artist)

        if not valid_albums:
            return None

        valid_album_titles = [clean_text(x.title) for x in valid_albums]

        valid_songs = []

        existing_songs = []
        if db_artist:
            if db_artist.id:
                db_songs: List[Song] = Song.find_songs_by_artist(session, db_artist.id)
                if db_songs:
                    for db_song in db_songs:
                        if db_song.title:
                            existing_songs.append(db_song.title)

        for va in valid_albums:
            if va.tracks:
                for track in va.tracks:
                    if track.title:
                        exists = False
                        for e_song in existing_songs:
                            if compare_strings(e_song, track.title):
                                exists = True
                        if not exists:
                            valid_songs.append(remove_punc(track.title))

        if logger.is_logging():
            logger.log_title(LOGGER, 'Valid song titles:')
            for s_title in valid_songs:
                logger.debug(LOGGER, s_title)

        genius_artist, genius_songs = get_songs_from_genius(artist)

        if not db_artist:
            s_artist = create_artist_for_db(genius_artist, mb_artist)
            db_artist = insert_artist(session, s_artist)

        albums = {}

        num_threads = 15

        songs_chunks = list(divide_chunks(genius_songs, ((len(genius_songs) // num_threads) + 1)))

        processes = []

        songs_list = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for song_list in songs_chunks:
                processes.append(executor.submit(thread_songs, song_list, db_artist.id, db_artist.name))

        for task in as_completed(processes):
            songs_list.extend(task.result())

        if logger.is_logging():
            logger.log_title(LOGGER, 'Missing Titles')

            _songs_titles = [x.title for x in genius_songs]
            song_list_titles = [y.title for y in songs_list]
            for tit in _songs_titles:
                if tit not in song_list_titles:
                    logger.debug(LOGGER, tit)

            logger.log_title(LOGGER, 'All Titles')
            for tit in _songs_titles:
                logger.debug(LOGGER, tit)

        remaining_albums = {}

        for _song in songs_list:
            if _song.album:
                c_album = clean_text(_song.album)
                if c_album in valid_album_titles:
                    if _song.album not in albums:
                        albums[_song.album] = []
                    albums[_song.album].append(_song)
                else:
                    if _song.album not in remaining_albums:
                        remaining_albums[_song.album] = []
                    remaining_albums[_song.album].append(_song)
                    logger.debug(LOGGER, "Album wasn't found in valid album titles: {}".format(c_album))

        valid_matches = []

        for album_key in albums.keys():
            a_key = clean_text(album_key)
            if a_key in valid_album_titles:
                valid_album = get_valid_album(valid_albums, a_key)
                build_album_data(session, db_artist.id, album_key, albums[album_key], valid_album, db_artist.name)
                valid_matches.append(a_key)

        missing_valid_matches = list(set(valid_album_titles).difference(valid_matches))

        for ra_key in remaining_albums.keys():
            found = 0
            match = None
            for mvm in missing_valid_matches:
                if remove_punc(clean_text(mvm)) in remove_punc(clean_text(ra_key)):
                    found = found + 1
                    match = mvm
            if found == 1 and match:
                valid_album = get_valid_album(valid_albums, match)
                build_album_data(session, db_artist.id, match.title(), remaining_albums[ra_key], valid_album,
                                 db_artist.name)
            else:
                logger.debug(LOGGER,
                             '{} was not found in valid or remaining albums {}'.format(ra_key, remaining_albums.keys()))

        logger.info(LOGGER, 'artist data built {}'.format(artist))


def build_artists_from_list():
    create_tables(get_sql_file())
    logger.set_logging(False)

    start = time.time()
    initialize()
    # build_artist_data('+44')

    for artist in ARTISTS:
        build_artist_data(artist)
        time.sleep(30)
    end = time.time()

    elapsed = end - start

    print('Total elapsed: {}'.format(elapsed))


if __name__ == '__main__':
    artist, songs = get_songs_from_genius('Silverstein')
    print('debug')

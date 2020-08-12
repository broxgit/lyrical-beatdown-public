import logging
from typing import List

from database.sql_alchemy.declarative import Album, Artist, Song
from database.sql_alchemy.sa_utils import managedSession, initialize
from database.sqlite_util import *
from main.build_data import build_artist_data
from logger import logger

from app.album_lyrics import ArtistData, AlbumData

LOGGER = logger.setup_logger('root', logging.DEBUG)


def get_album_by_artist(album_name, artist_name):
    with managedSession() as session:
        _artist = Artist.find_by_name(session, artist_name)

        if not _artist:
            return None
        if not _artist.id:
            return None

        _album = Album.find_by_name(session, album_name, _artist.id)

        return _album


def update_albums_with_artist():
    _albums = get_all_albums()
    with managedSession() as session:
        for album in _albums:
            _artist = Artist.find_by_id(session, album.artist_id)
            album.artist_name = _artist.name
            session.commit()


def update_all_with_word_count():
    with managedSession() as session:
        artists = get_all_artists()
        for artist in artists:
            albums: List[Album] = get_all_artist_albums(artist.id)
            if albums:
                for album in albums:
                    if album:
                        songs: List[Song] = get_all_album_songs(album.id)
                        if songs:
                            for song in songs:
                                lyrics_list = song.lyrics.split()
                                song.word_count = len(lyrics_list)
                                session.commit()
                        alb_lyrics_list = album.total_words.split()
                        album.word_count = len(alb_lyrics_list)
                        session.commit()
            art_lyrics_list = artist.total_words.split()
            artist.word_count = len(art_lyrics_list)
            session.commit()


def get_all_albums():
    with managedSession() as session:
        _albums = Album.get_all_albums(session)
        return _albums


def get_all_artists():
    with managedSession() as session:
        _artists = Artist.get_all_artists(session)
        return _artists


def get_artist_by_name(artist_name):
    with managedSession() as session:
        _artist = Artist.find_by_name(session, artist_name)
        if _artist:
            return _artist
    return None


def get_all_artist_albums(artist_id):
    with managedSession() as session:
        _albums = Album.find_albums_by_artist(session, artist_id)
        return _albums


def get_all_album_songs(album_id):
    with managedSession() as session:
        songs = Song.find_songs_by_album(session, album_id)
        return songs


def artist_album_words(artist, web_request=False):
    with managedSession() as session:
        _artist = Artist.find_by_name(session, artist)

        if not _artist:
            return None

        if not _artist.id:
            return None

        albums = Album.find_albums_by_artist(session, _artist.id)
        if not albums:
            return None
        album_list: List[AlbumData] = []
        for album in albums:
            album_list.append(AlbumData(album_data=album, song_list=[]))
        artist_data = ArtistData(_artist, album_list)
    if web_request:
        return artist_data

    # write_to_csv(artist, album_word_list)


def db_init():
    conn = create_connection()
    create_artists_table(conn)
    create_albums_table(conn)
    create_songs_table(conn)


def build_and_test(artist_name):
    build_artist_data(artist_name)
    artist_album_words(artist_name)


def clear_artist_entries(artist_name):
    with managedSession() as session:
        artist = Artist().find_by_name(session, artist_name)
        Song().remove_songs_by_artist(session, artist.id)
        Album().remove_album_by_artist(session, artist.id)


if __name__ == '__main__':
    logger.set_logging(False)
    initialize()

    update_all_with_word_count()

    # res = artist_album_words('Silverstein', True)
    # create_tables(get_sql_file())
    #
    # update_albums_with_artist()

    # test_db()
    # test_db_update()

    # session = managedSession()
    # artist = Artist().find_by_name(session, 'Taylor Swift')
    # Song().remove_songs_by_artist(session, artist.id)
    # Album().remove_album_by_artist(session, artist.id)
    # clear_artist_entries('Silverstein')
    # build_and_test('Taylor Swift')
    # create_tables(sql_file())
    # artist = search_artist('Silverstein')
    # serialize_artist(artist)
    # pass

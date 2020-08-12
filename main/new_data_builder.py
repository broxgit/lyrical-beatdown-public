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
from main.get_data import get_all_artists, get_all_artist_albums
from music_brainz.get_data import get_artist_albums_from_mb, get_artist_data
from music_brainz.models.album import Album as Mb_Album
from utils.misc_utils import *
from main.build_data import get_songs_from_genius, get_artist_from_genius

LOGGER = logger.setup_logger('root', logging.DEBUG)


def build_with_existing(db_artist, genius_artist, mb_artist, valid_albums):
    albums: List[Album] = get_all_artist_albums(db_artist.id)

    new_albums = []

    for va in valid_albums:
        exists = False
        for album in albums:
            if compare_strings(va.mb_data.title, album.name):
                exists = True
                break
        if not exists:
            new_albums.append(va)

    if len(new_albums) == 0:
        return None

    build_artist_albums(new_albums, mb_artist, genius_artist)


def build_artist_albums(valid_albums, mb_artist, genius_artist):
    genius_songs = get_songs_from_genius(mb_artist.name)

    new_genius_songs = []

    for new_album in valid_albums:
        for track in new_album.tracks:
            db_song = Song()
            exists = False
            for song in genius_songs:
                if compare_strings(song.title, track.title):
                    pass


def build_from_scratch(genius_artist, mb_artist, valid_albums):
    db_album: Album = Album()
    build_artist_albums(valid_albums, mb_artist, genius_artist)


def new_build(artist_name):
    # Get Artist and Songs from Genius API
    genius_artist = get_artist_from_genius(artist_name)
    #
    # If Genius API doesn't contain artist data, return None
    if not genius_artist:
        logger.error(LOGGER, 'Artist data not found via Genius API: {}'.format(artist_name))
        return None

    # Get Artist from MusicBrainz Database
    mb_artist = get_artist_data(artist_name)

    # If Artist doesn't exist in MusicBrainz Database, return None
    if not mb_artist:
        logger.error(LOGGER, 'Artist data not found in MusicBrainz database: {}'.format(artist_name))
        return None

    # Generate a list of valid albums
    valid_albums = get_artist_albums_from_mb(mb_artist)

    # If no valid albums exist for the artist, return None
    if not valid_albums:
        return None
    #
    with managedSession() as session:
        # Check if artist already exists in the database
        db_artist = Artist.find_by_name(session, genius_artist)
        if db_artist:
            build_with_existing(db_artist, genius_artist, mb_artist, valid_albums)
        else:
            build_from_scratch(genius_artist, mb_artist, valid_albums)


if __name__ == '__main__':
    logger.set_logging(False)
    initialize(get_sql_file())
    with managedSession() as session:
        artists: List[Artist] = get_all_artists()
        for artist in artists:
            new_build(artist.name)


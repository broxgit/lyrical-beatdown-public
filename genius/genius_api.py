import logging
import time

import lyricsgenius

from api_keys import GENIUS_API_KEY
from genius.models.genius_song import GeniusSong
from logger import logger

LOGGER = logger.setup_logger('root', logging.DEBUG)


def get_api_object():
    genius = lyricsgenius.Genius(GENIUS_API_KEY, sleep_time=1)
    genius.remove_section_headers = True
    genius.skip_non_songs = True
    # genius.verbose = False

    return genius


def search_artist(artist):
    genius = get_api_object()

    _artist = genius.search_artist(artist, sort="title", max_songs=1)

    return _artist


def search_song(song_title, artist):
    genius = get_api_object()

    try:
        _song = genius.search_song(song_title, artist)
    except Exception as e:
        logger.info(LOGGER, "Exception caught ({})  when searching for song {}".format(e, song_title))
        time.sleep(10)
        try:
            _song = genius.search_song(song_title, artist)
        except TypeError as te:
            logger.error(LOGGER, 'TypeError encountered when trying to get {} from Genius'.format(song_title))
            return None

    return _song


def get_artist_songs(artist_id: int, page: int) -> dict:
    genius = get_api_object()

    _songs = genius.get_artist_songs(artist_id, page=page)

    return _songs


def get_song(song_id: int):
    genius = get_api_object()

    song = genius.get_song(song_id)
    return song['song']


if __name__ == '__main__':
    song = get_song(254611)
    # d = song.to_dict()
    gs: GeniusSong = GeniusSong().from_dict(song)
    print('debug')

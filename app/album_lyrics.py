from typing import List

from database.sql_alchemy.declarative import Song, Album, Artist


class AlbumData(object):
    data: Album = None
    songs: List[Song]

    def __init__(self, album_data, song_list):
        self.data = album_data
        self.songs = song_list


class ArtistData(object):
    data: Artist = None
    albums: List[AlbumData]

    def __init__(self, artist, album_list):
        self.data = artist
        self.albums = album_list

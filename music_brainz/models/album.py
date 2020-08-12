from typing import List

from music_brainz.models.release import Release, TrackList


class Track(object):
    def __init__(self, id, title, length, disambiguation, number, mb_data: TrackList):
        self.id = id
        self.title = title
        self.length = length
        self.disambiguation = disambiguation
        self.number = number
        self.mb_data = mb_data


class AlbumArt(object):
    a250: str = None
    a500: str = None
    a1200: str = None

    def __init__(self, a250, a500, a1200):
        self.a250 = a250
        self.a500 = a500
        self.a1200 = a1200


class Album(object):
    id = None
    artist = None
    tracks: List[Track] = None
    bonus_tracks: List[Track] = None
    album_art: AlbumArt = None
    label = None
    mb_data: Release = None

    def __init__(self):
        pass

    def from_mb_release(self, mb_release: Release, album_art_urls=None, artist_name=None, tracks=None, bonus_tracks=None):
        self.mb_data = mb_release

        if artist_name:
            self.artist = artist_name

        self.tracks: List[Track] = []

        self.bonus_tracks = bonus_tracks

        self.tracks = tracks

        if mb_release.label_info_count > 0:
            for l in mb_release.label_info_list:
                if l.label:
                    if l.label.name:
                        self.label = l.label.name
                        break
        if album_art_urls:
            a250 = ''
            a500 = ''
            a1200 = ''
            if '1200' in album_art_urls:
                a1200 = album_art_urls['1200']
            if '500' in album_art_urls:
                a500 = album_art_urls['500']
            elif 'large' in album_art_urls:
                a500 = album_art_urls['large']
            if '250' in album_art_urls:
                a250 = album_art_urls['250']
            elif 'small' in album_art_urls:
                a250 = album_art_urls['small']
            self.album_art = AlbumArt(a250, a500, a1200)

        return self



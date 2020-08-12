from database.sql_alchemy.declarative import *
from music_brainz.models.artist_results import ArtistResult
from utils.misc_utils import normalize_unicode
from music_brainz.models.album import Album as Mb_Album, Track
from lyricsgenius.song import Song as GSong


def create_artist_for_db(genius_artist, mb_artist: ArtistResult):
    new_artist = Artist(
        name=normalize_unicode(genius_artist.name),
        genius_id=genius_artist._id,
        image_url=genius_artist.image_url,
        mb_data=mb_artist.to_dict(),
        mb_id=mb_artist.id,

    )

    return new_artist


def create_album_for_db(artist_id, valid_album: Mb_Album, artist_name):
    a250 = ''
    a500 = ''
    a1200 = ''
    label = ''
    if valid_album.album_art:
        a250 = valid_album.album_art.a250
        a500 = valid_album.album_art.a500
        a1200 = valid_album.album_art.a1200

    if valid_album.label:
        label = valid_album.label
    else:
        print('debug')
    new_album = Album(
        name=valid_album.mb_data.title,
        artist_id=artist_id,
        year=valid_album.mb_data.date.year,
        label=label,
        album_art_250=a250,
        album_art_500=a500,
        album_art_1200=a1200,
        mb_id=valid_album.mb_data.id,
        music_brainz_data=valid_album.mb_data.to_dict(),
        artist_name=artist_name
    )

    return new_album


def create_song_for_db(song: GSong, artistId, albumId, mb_track: Track):
    new_song = Song(
        title=song.title,
        lyrics=song.lyrics,
        genius_id=song._id,
        artist_id=artistId,
        album_id=albumId,
        genius_data=song.to_dict(),
        music_brainz_data=mb_track.mb_data.to_dict()
    )

    return new_song

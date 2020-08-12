from typing import List

from database.sql_alchemy.declarative import Artist, Album, Song
# from database.sql_alchemy.declarative_new import Artist as ArtistNew, Album as AlbumNew, Song as SongNew, create_tables
from database.sql_alchemy.insert import insert_song, insert_album, insert_artist
from database.sql_alchemy.sa_utils import managedSession, initialize
from main.get_data import get_all_artists, get_all_artist_albums, get_all_album_songs
from music_brainz.get_data import get_artist_data
from music_brainz.models.artist_results import ArtistResult
from main.count_words import count_words_simple, count_words_complex
from utils.misc_utils import prcnt
from utils.misc_utils import merge_dict


def migrate_database():
    with managedSession() as session:
        artists: List[Artist] = get_all_artists()
        for artist in artists:
            artist_mb_id = None

            mb_data: ArtistResult = get_artist_data(artist.name)
            if mb_data:
                artist_mb_id = mb_data.id

            else:
                print('{} not found from MB!'.format(artist.name))
                exit(1)

            albums: List[Album] = get_all_artist_albums(artist.id)
            artist_simple_words = {}
            artist_complex_words = {}
            total_artist_words = []

            if not albums:
                print('{} has no albums!'.format(artist.name))
                continue

            for album in albums:
                album_simple_words = {}
                album_complex_words = {}
                total_album_words = []
                songs: List[Song] = get_all_album_songs(album.id)
                if not songs:
                    print('{} -- {} has no songs'.format(artist.name, album.name))
                    continue
                for song in songs:
                    # if SongNew.find_by_name(session, song.title, artist.id):
                    #     print('{} already exists -- skipping'.format(song.title))
                    #     continue
                    mb_id = ''
                    duration = 1

                    if song.music_brainz_data:
                        if 'id' in song.music_brainz_data:
                            mb_id = song.music_brainz_data['id']
                        if 'length' in song.music_brainz_data:
                            duration = song.music_brainz_data['length']
                        if not duration:
                            if 'recording' in song.music_brainz_data:
                                recording = song.music_brainz_data['recording']
                                if recording:
                                    if 'length' in recording:
                                        duration = recording['length']

                    song_words = song.lyrics.split()
                    simple_counter = count_words_simple(song.lyrics)
                    complex_counter = count_words_complex(song.lyrics)

                    simple_dict = dict(simple_counter)
                    complex_dict = dict(complex_counter)

                    song_percent_simple = prcnt(len(simple_dict), len(song_words))
                    song_percent_complex = prcnt(len(complex_dict), len(song_words))

                    db_song = Song(
                        title=song.title,
                        has_lyrics=True,
                        lyrics=song.lyrics,
                        is_bonus_track=False,
                        duration=duration,
                        mb_id=mb_id,
                        music_brainz_data=song.music_brainz_data,
                        genius_id=song.genius_id,
                        genius_data=song.genius_data,
                        unique_simple=simple_dict,
                        unique_complex=complex_dict,
                        percent_simple=song_percent_simple,
                        percent_complex=song_percent_complex,
                        total_simple=len(simple_dict),
                        total_complex=len(complex_dict),
                        artist_id=song.artist_id,
                        album_id=song.album_id
                    )

                    insert_song(session, db_song)

                    album_simple_words = merge_dict(simple_dict, album_simple_words)
                    album_complex_words = merge_dict(complex_dict, album_complex_words)
                    total_album_words.extend(song_words)

                album_percent_simple = prcnt(len(album_simple_words), len(total_album_words))
                album_percent_complex = prcnt(len(album_complex_words), len(total_album_words))
                total_album_words_str = ' '.join(total_album_words)

                db_album = Album(
                    id=album.id,
                    name=album.name,
                    year=album.year,
                    label=album.label,
                    album_art=album_art,
                    mb_id=album.mb_id,
                    music_brainz_data=album.music_brainz_data,
                    artist_name=album.artist_name,
                    artist_id=album.artist_id,
                    total_words=total_album_words_str,
                    unique_simple=album_simple_words,
                    unique_complex=album_complex_words,
                    percent_simple=album_percent_simple,
                    percent_complex=album_percent_complex,
                    total_simple=len(album_simple_words),
                    total_complex=len(album_complex_words)
                )

                insert_album(session, db_album)

                artist_simple_words = merge_dict(album_simple_words, artist_simple_words)
                artist_complex_words = merge_dict(album_complex_words, artist_complex_words)
                total_artist_words.extend(total_album_words)

            if len(total_artist_words) == 0:
                continue

            artist_percent_simple = prcnt(len(artist_simple_words), len(total_artist_words))
            artist_percent_complex = prcnt(len(artist_complex_words), len(total_artist_words))
            total_artist_words_words_str = ' '.join(total_artist_words)

            db_artist = Artist(
                id=artist.id,
                name=artist.name,
                image_url=artist.image_url,
                mb_id=artist_mb_id,
                genius_id=artist.genius_id,
                mb_data=mb_data.to_dict(),
                total_words=total_artist_words_words_str,
                unique_simple=artist_simple_words,
                unique_complex=artist_complex_words,
                percent_simple=artist_percent_simple,
                percent_complex=artist_percent_complex,
                total_simple=len(artist_simple_words),
                total_complex=len(artist_complex_words)
            )

            insert_artist(session, db_artist)

            print('Finished building {}'.format(artist.name))


if __name__ == '__main__':
    create_tables("sqlite:///../../resources/sqlite.db")
    initialize()
    migrate_database()

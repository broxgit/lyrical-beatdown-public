import tekore as tk
from tekore.model import FullArtist

from api_keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

if __name__ == '__main__':
    app_token = tk.request_client_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    spotify = tk.Spotify(app_token)

    res = spotify.search('Silverstein', ('artist',))
    for result in res:
        for a in result.items:
            a: FullArtist = a
            if a.name == 'Silverstein':
                art = spotify.artist(a.id)
                art_albums = spotify.artist_albums(a.id)
                album = spotify.album_tracks('6HtcHNGQ9CNGisIS7DlMLW')
                track = spotify.track('2DADATOYLLFrNlp6jN6J4t')
                print('debug')

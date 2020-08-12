#!/usr/bin/env python3

import connexion
from connexion import NoContent

from database.sql_alchemy.declarative import Artist
from database.sql_alchemy.sa_utils import managedSession
from main.get_data import artist_album_words

from api import encoder


def get_artist_by_name(artistName):  # noqa: E501
    """Get lyrical data for artist

     # noqa: E501

    :param artist_name:
    :type artist_name: str

    :rtype: ArtistAlbums
    """

    # artist = artistName
    #
    # if isinstance(artistName, dict):
    #     json_data = json.dumps(artistName)
    #     artist = json_data['artist']
    with managedSession() as session:
        _artist = Artist.find_by_name(session, artistName)
    if not _artist:
        return NoContent, 404

    return artist_album_words(artistName, web_request=True)


app = connexion.FlaskApp(__name__)
app.add_api('api/swagger.yaml')
app.app.json_encoder = encoder.JSONEncoder
application = app.app


def main():
    app.run(port=54321, use_reloader=False, threaded=False)


if __name__ == '__main__':
    main()

# import cProfile
# import operator

from flask import render_template, request, Flask
# from flask_mail import Mail
# import sqlalchemy
# import flask_profiler

from database.sql_alchemy.declarative import create_tables, Album
from database.sql_alchemy.sa_utils import initialize, get_sql_file
from main.get_data import artist_album_words, get_album_by_artist, get_all_albums, get_all_artists, get_artist_by_name, \
    get_all_album_songs
from utils.misc_utils import compare_strings


app = Flask(__name__, template_folder='templates', static_folder='static')
# app.config["DEBUG"] = True
#
# app.config["flask_profiler"] = {
#     "verbose": True,
#     "enabled": app.config["DEBUG"],
#     "storage": {
#         "engine": "sqlalchemy",
#         "db_url": "sqlite:///flask_profiler.db"  # optional
#     },
#     "basicAuth": {
#         "enabled": False
#     }
# }

initialize()
create_tables(get_sql_file())

# mail = Mail()
#
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USE_SSL"] = True
# app.config["MAIL_USERNAME"] = 'contact@example.com'
# app.config["MAIL_PASSWORD"] = 'your-password'
#
# mail.init_app(app)

# flask_profiler.init_app(app)


@app.route('/index')
@app.route('/', methods={'GET'})
def home():
    return render_template('index.html')


@app.route('/artist', methods={'POST', 'GET'})
# @flask_profiler.profile()
def browse_artists():
    if request.method == 'GET':
        artists = get_all_artists()
        return render_template('browse.html', title='Browse Artists Collection', artists=artists)


@app.route('/artist/<string:artist>', methods={'GET'})
# @flask_profiler.profile()
def get_artist(artist):
    artist_data = artist_album_words(artist, web_request=True)
    if not artist_data:
        artist_data = artist_album_words(artist.replace('_', '/'), web_request=True)
    if not artist_data:
        return render_template('artist.html', title='Not Found', artist=None, notFound=artist)
    else:
        sorted_simple = artist_data.data.unique_simple
        sorted_complex = artist_data.data.unique_complex
        return render_template('artist.html', title='{} Results'.format(artist), artist=artist_data,
                               top20simple=sorted_simple, top20complex=sorted_complex)


@app.route('/album', methods={'POST', 'GET'})
# @flask_profiler.profile()
def browse_albums():
    if request.method == 'GET':
        albums = get_all_albums()
        return render_template('browse.html', title='Browse Album Collection', albums=albums)


@app.route('/ohBear')
def oh_bear():
    return render_template('oh_bear.html', title='Placeholder for Video of Axel Dancing')


@app.route('/artist/<string:artist>/album/<string:album_name>')
# @flask_profiler.profile()
def get_album(artist, album_name):
    album_db: Album = get_album_by_artist(album_name, artist.replace('_', '/'))
    if not album_db:
        return render_template('artist.html', title='Not Found', results=None, notFound=album_name)
    else:
        album_image = album_db.album_art['250']
        album_label = album_db.label
        songs = get_all_album_songs(album_db.id)

        return render_template('album.html', title='Album Breakdown', album=album_db, top20complex=album_db.unique_complex,
                               top20simple=album_db.unique_simple, album_image=album_image, album_label=album_label,
                               songs=songs)


@app.route('/contact_form', methods={'GET'})
def contact_form():
    return render_template('request_form.html')


if __name__ == '__main__':
    app.run()

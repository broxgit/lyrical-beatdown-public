import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to a SQLite database """
    db_file = r"../resources/sqlite.db"

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # conn.set_trace_callback(print)
    except Error as e:
        print(e)

    return conn


def get_db_entity(conn, sql_statement, entity):
    cur = conn.cursor()

    try:
        cur.execute(sql_statement, (entity,))
    except sqlite3.OperationalError as e:
        return None

    conn.commit()

    rows = cur.fetchall()

    return rows


def create_db_entity(conn, sql_statement, entity):
    cur = conn.cursor()
    try:
        cur.execute(sql_statement, entity)
    except sqlite3.OperationalError as oe:
        print(oe)
    except Exception as e:
        print(e)
    conn.commit()
    return cur.lastrowid


def get_all_album_songs(conn, album):
    _album = album_exists(conn, album)
    if _album:
        album_id = _album[0][0]
        sql = """SELECT * FROM songs WHERE album_id=?"""
        _songs = get_db_entity(conn, sql, album_id)
        return _songs
    else:
        print("Album doesn't exist in database...")
        return None


def get_all_artist_albums(conn, artist):
    _artist = artist_exists(conn, artist)
    if _artist:
        artist_id = _artist[0][0]
        sql = """SELECT * FROM albums WHERE artist_id=?"""
        _songs = get_db_entity(conn, sql, artist_id)
        return _songs
    else:
        print("Album doesn't exist in database...")
        return None


def artist_exists(conn, artist):
    sql = """SELECT * FROM artists WHERE name=?"""
    _artist = get_db_entity(conn, sql, artist)
    if not _artist:
        return False
    if len(_artist) < 1:
        return False
    return _artist


def song_exists(conn, song_title):
    sql = '''SELECT * FROM songs WHERE title=?'''
    song = get_db_entity(conn, sql, song_title)
    if not song:
        return False
    if len(song) < 1:
        return False
    return song


def album_exists(conn, album):
    sql = '''SELECT * FROM albums WHERE name=?'''
    _album = get_db_entity(conn, sql, album)
    if not _album:
        return False
    if len(_album) < 1:
        return False
    return _album


def create_artists_table(conn):
    sql_create_artists_table = """CREATE TABLE IF NOT EXISTS artists (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            genius_id integer NOT NULL
                                        );"""
    create_table(conn, sql_create_artists_table)


def create_albums_table(conn):
    sql_create_albums_table = """CREATE TABLE IF NOT EXISTS albums (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        artist_id integer NOT NULL,
                                        FOREIGN KEY (artist_id) REFERENCES artists (id)
                                    );"""
    create_table(conn, sql_create_albums_table)


def create_songs_table(conn):
    sql_create_songs_table = """ CREATE TABLE IF NOT EXISTS songs (
                                           id integer PRIMARY KEY,
                                           title text,
                                           artist text,
                                           album text,
                                           lyrics text,
                                           artist_id integer NOT NULL,
                                           album_id integer NOT NULL,
                                           FOREIGN KEY (artist_id) REFERENCES artists (id),
                                           FOREIGN KEY (album_id) REFERENCES albums (id)
                                       ); """
    create_table(conn, sql_create_songs_table)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)


def create_song(conn, song):
    sql = ''' INSERT INTO songs(title,artist,album,lyrics,artist_id,album_id) 
              VALUES(?,?,?,?,?,?) '''
    return create_db_entity(conn, sql, song)


def create_artist(conn, artist):
    sql = ''' INSERT INTO artists(name,genius_id) 
                  VALUES(?,?) '''
    return create_db_entity(conn, sql, artist)


def create_album(conn, album):
    sql = ''' INSERT INTO albums(name,artist_id) 
              VALUES(?,?) '''
    return create_db_entity(conn, sql, album)


if __name__ == '__main__':
    create_connection()

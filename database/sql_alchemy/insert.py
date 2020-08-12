def insert_artist(session, artist):
    _insert(session, artist)
    return artist


def insert_album(session, album):
    _insert(session, album)
    return album


def insert_song(session, song):
    _insert(session, song)
    return song


def insert_test(session, test):
    _insert(session, test)
    return test


def _insert(session, obj):
    session.add(obj)
    session.flush()
    session.commit()

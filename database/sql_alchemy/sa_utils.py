import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session

ENGINE = None
SCOPED_SESSION = None


def get_sql_file():
    import os
    file_path = os.path.abspath('../resources/sqlite.db')
    return "sqlite:///{}".format(file_path)


def initialize(sql_file=None):
    if not sql_file:
        sql_file = get_sql_file()

    global ENGINE
    if not ENGINE:
        ENGINE = create_engine(sql_file, convert_unicode=True)


def get_session():
    from sqlalchemy.orm import sessionmaker

    global ENGINE

    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

    session.expire_on_commit = False

    return session


@contextlib.contextmanager
def managedSession():
    from sqlalchemy.orm import sessionmaker

    global SCOPED_SESSION

    if not SCOPED_SESSION:
        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
        SCOPED_SESSION = scoped_session(session_factory)
        SCOPED_SESSION.expire_on_commit = False

    session = SCOPED_SESSION()

    try:
        yield session
    except Exception:
        session.rollback()
        raise

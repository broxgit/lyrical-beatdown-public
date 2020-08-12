from sqlalchemy import create_engine, func, DateTime, Numeric,  Boolean
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from database.sql_alchemy.testes import JsonEncodedDict


Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artist'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    genius_id = Column(Integer, nullable=False)
    mb_id = Column(String(250), nullable=False)
    image_url = Column(Text)
    mb_data = Column(JsonEncodedDict)

    total_words = Column(Text)
    word_count = Column(Integer)
    unique_simple = Column(JsonEncodedDict)
    unique_complex = Column(JsonEncodedDict)
    percent_simple = Column(Numeric(4, 2))
    percent_complex = Column(Numeric(4, 2))
    total_simple = Column(Integer)
    total_complex = Column(Integer)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def get_all_artists(cls, session):
        obj = session.query(cls).all()
        if len(obj) == 0:
            return None
        else:
            return obj

    @classmethod
    def find_by_name(cls, session, name):
        obj = session.query(cls).filter(func.lower(Artist.name) == func.lower(name)).first()
        return obj

    @classmethod
    def find_by_id(cls, session, id):
        obj = session.query(cls).get(id)
        return obj


class Album(Base):
    __tablename__ = 'album'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    year = Column(Integer)

    album_art = Column(JsonEncodedDict)

    mb_id = Column(String(250))
    label = Column(Text)
    music_brainz_data = Column(JsonEncodedDict)

    total_words = Column(Text)
    word_count = Column(Integer)
    unique_simple = Column(JsonEncodedDict)
    unique_complex = Column(JsonEncodedDict)
    percent_simple = Column(Numeric(4, 2))
    percent_complex = Column(Numeric(4, 2))
    total_simple = Column(Integer)
    total_complex = Column(Integer)

    artist_name = Column(Text)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship(Artist)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


    @classmethod
    def find_by_name(cls, session, name, artist_id):
        obj = session.query(cls).filter_by(name=name, artist_id=artist_id).all()
        if len(obj) == 0:
            return None
        elif len(obj) == 1:
            return obj[0]
        else:
            print('More than one Album found matching the criteria provided')
            return obj

    @classmethod
    def get_all_albums(cls, session):
        obj = session.query(cls).all()
        if len(obj) == 0:
            return None
        else:
            return obj

    @classmethod
    def find_albums_by_artist(cls, session, artist_id):
        obj = session.query(cls).filter_by(artist_id=artist_id).all()
        if len(obj) == 0:
            return None
        else:
            return obj

    @classmethod
    def remove_album_by_artist(cls, session: Session, artist_id):
        albums = session.query(cls).filter_by(artist_id=artist_id).all()
        if len(albums) == 0:
            return
        else:
            for a in albums:
                session.delete(a)
                session.commit()


class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    has_lyrics = Column(Boolean)
    lyrics = Column(Text)
    is_bonus_track = Column(Boolean)
    duration = Column(Integer)

    mb_id = Column(Integer)
    music_brainz_data = Column(JsonEncodedDict)

    genius_id = Column(Integer, nullable=False)
    genius_data = Column(JsonEncodedDict)

    # total_words = Column(Text)
    word_count = Column(Integer)
    unique_simple = Column(JsonEncodedDict)
    unique_complex = Column(JsonEncodedDict)
    percent_simple = Column(Numeric(4, 2))
    percent_complex = Column(Numeric(4, 2))
    total_simple = Column(Integer)
    total_complex = Column(Integer)

    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship(Artist)

    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship(Album)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def find_by_name(cls, session, title, artist_id):
        obj = session.query(cls).filter_by(title=title, artist_id=artist_id).all()
        if len(obj) == 0:
            return None
        elif len(obj) == 1:
            return obj[0]
        else:
            print('More than one Song found matching the name criteria provided')
            return obj

    @classmethod
    def find_songs_by_album(cls, session, album_id):
        obj = session.query(cls).filter_by(album_id=album_id).all()
        if len(obj) == 0:
            return None
        else:
            return obj

    @classmethod
    def find_songs_by_artist(cls, session, artist_id):
        obj = session.query(cls).filter_by(artist_id=artist_id).all()
        if len(obj) == 0:
            return None
        else:
            return obj

    @classmethod
    def remove_songs_by_artist(cls, session: Session, artist_id):
        songs = session.query(cls).filter_by(artist_id=artist_id).all()
        if len(songs) == 0:
            return
        else:
            for s in songs:
                session.delete(s)
                session.commit()


def create_tables(sqlite_file):
    engine = create_engine(sqlite_file)
    Base.metadata.create_all(engine)
    engine.dispose()


if __name__ == '__main__':
    create_tables("sqlite:///../../resources/sqlite.db")


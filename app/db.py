from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
import config
from sqlalchemy.orm import sessionmaker


engine = create_engine(config.DATABASE_URI)

base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class MusicTracks(base):
    __tablename__ = 'music_tracks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    genre = Column(String)
    release_year = Column(Integer)
    duration = Column(Integer)
    path_key = Column(String)

    def __init__(self, title, artist, album, genre, release_year, duration, path_key):
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.release_year = release_year
        self.duration = duration
        self.path_key = path_key


class Playlists(base):

    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __init__(self, title):
        self.title = title


class PlaylistDetails(base):

    __tablename__ = 'playlist_details'
    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True)
    music_track_id = Column(Integer, ForeignKey('music_tracks.id'), primary_key=True)

    def __init__(self, playlist_id, music_track_id):
        self.playlist_id = playlist_id
        self.music_track_id = music_track_id


def add_record(new_record):
    session.add(new_record)
    session.commit()


def delete_record(record):
    session.delete(record)


def record_commit():
    session.commit()


def all_tracks():
    '''select all music tracks in music tracks table'''
    records = session.query(MusicTracks).all()
    return records


def track_by_id(record_id):
    '''select music tracks by id in music tracks table'''
    record = session.query(MusicTracks).filter(MusicTracks.id == record_id).first()
    return record


# def search_track_details_by_title_artist(search_input: str):
#     records = session.query(MusicTracks).filter(
#         MusicTracks.title.like(f'%{search_input}%') | MusicTracks.artist.like(f'%{search_input}%')).all()
#     return records

def all_playlists():
    '''select all playlists in playlists table'''
    records = session.query(Playlists).all()
    return records


def playlist_by_id(record_id):
    '''select playlists by id in playlists table'''
    record = session.query(Playlists).filter(Playlists.id == record_id).first()
    return record


def tracks_playlist(playlist_id):
    '''select all music track in one playlist'''
    records = session.query(MusicTracks).filter(MusicTracks.id == PlaylistDetails.music_track_id,
                                                PlaylistDetails.playlist_id == playlist_id).all()

    return records


def track_in_playlist(playlist_id, track_id):
    '''check an existing track in a playlist'''
    record = session.query(PlaylistDetails).filter(PlaylistDetails.music_track_id == track_id,
                                            PlaylistDetails.playlist_id == playlist_id).first()
    return record


def search_track_details_by_title(search_input: str):
    '''select all music track by track title'''
    records = session.query(MusicTracks).filter(MusicTracks.title.like(f'%{search_input}%')).all()
    return records


def search_track_details_by_artist(search_input: str):
    '''select all music track by track artist'''
    records = session.query(MusicTracks).filter(MusicTracks.artist.like(f'%{search_input}%')).all()
    return records


def search_track_details_by_album(search_input: str):
    '''select all music track by track album'''
    records = session.query(MusicTracks).filter(MusicTracks.album.like(f'%{search_input}%')).all()
    return records


def search_track_details_by_genre(search_input: str):
    '''select all music track by track genre'''
    records = session.query(MusicTracks).filter(MusicTracks.genre.like(f'%{search_input}%')).all()
    return records


def playlist_by_ids(ids):
    '''select all playlists containing one of the query tracks'''
    records = session.query(Playlists).distinct(Playlists.id).filter(PlaylistDetails.playlist_id == Playlists.id,
                                    PlaylistDetails.music_track_id.in_(ids)).group_by(Playlists.id).all()
    return records

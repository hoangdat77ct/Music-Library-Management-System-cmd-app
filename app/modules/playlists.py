import db
import utilities
from config import playlist_options

def add_new_playlist() -> None:
    print(playlist_options['1'])
    print('Please enter the required information:')
    title = utilities.input_type(data_type=str, field='playlist name')
    if title:
        new_record = db.Playlists(title=title)
        db.add_record(new_record)
        print('Add new music track success!!')
    else:
        print('Failed because title is empty')


def delete_playlists() -> None:
    print(playlist_options['2'])
    playlist_records = db.all_playlists()
    playlist_empty = utilities.show_all_playlists(playlist_records)
    if playlist_empty:
        return
    ids = utilities.input_type(data_type=str, field='ids to remove separated by ","')
    ids = ids.split(',')
    if len(ids) > 0:
        for id in ids:
            temp_id = id.strip()
            try:
                record = db.playlist_by_id(int(temp_id))
                if record:
                    db.delete_record(record)
                    print(f'Deleted playlist ID: {temp_id}')
                else:
                    print(f'Playlist not found with ID: {temp_id}')
            except:
                print(f'Playlist not found with ID: {temp_id}')
        db.record_commit()
    return


def add_track_to_playlist():
    print(playlist_options['3'])
    playlist_records = db.all_playlists()
    playlist_empty = utilities.show_all_playlists(playlist_records)
    if playlist_empty:
        return
    playlist_id = utilities.input_type(data_type=int, field='playlist id')
    if playlist_id:
        record = db.playlist_by_id(playlist_id)
        if record:
            music_tracks = db.all_tracks()
            track_empty = utilities.show_all_tracks(music_tracks)
            if track_empty:
                return
            ids = utilities.input_type(data_type=str, field='track ids to add to the playlist separated by ","')
            ids = ids.split(',')
            if len(ids) > 0:
                for id in ids:
                    try:
                        track_id = int(id)
                    except:
                        print(f'Music track not found with ID: {id}')
                        continue
                    track_in_table = db.track_by_id(track_id)
                    if track_in_table:
                        track_exists = db.track_in_playlist(playlist_id, track_id)
                        if track_exists:
                            print(f'The track with the id ({id}) already exists in this playlist')
                        else:
                            new_record = db.PlaylistDetails(playlist_id=playlist_id, music_track_id=track_id)
                            db.add_record(new_record)
                            print(f'Add track with ID {track_id} to playlist successfully')
                    else:
                        print(f'Music track not found with ID: {id}')
        else:
            print(f'Playlist not found with ID: {playlist_id}')
    else:
        print('Playlist id takes only integer data value (>0)')


def delete_track_in_playlist():
    print(playlist_options['4'])
    playlist_records = db.all_playlists()
    playlist_empty = utilities.show_all_playlists(playlist_records)
    if playlist_empty:
        return
    playlist_id = utilities.input_type(data_type=int, field='playlist id')
    if  playlist_id:
        record = db.playlist_by_id(playlist_id)
        if record:
            music_tracks = db.tracks_playlist(playlist_id)
            track_empty = utilities.show_all_tracks(music_tracks)
            if track_empty:
                return
            ids = ids = utilities.input_type(data_type=str, field='track id to delete in playlist separated by ","')
            ids = ids.split(',')
            if len(ids) > 0:
                for id in ids:
                    temp_id = id.strip()
                    try:
                        record = db.track_in_playlist(playlist_id, int(temp_id))
                        if record:
                            db.delete_record(record)
                            print(f'Deleted music track with ID: {temp_id} in playlist')
                        else:
                            print(f'Music track not found with ID: {temp_id} in playlist')
                    except:
                        print(f'Music track not found with ID: {temp_id} in playlist')
                db.record_commit()
        else:
            print(f'Playlist not found with ID: {playlist_id}')
    else:
        print('Playlist id takes only integer data value (>0)')


def show_all_track_and_play(playlist_id):
    music_tracks = db.tracks_playlist(playlist_id)
    utilities.show_all_tracks(music_tracks)
    if music_tracks:
        utilities.handle_open_music(music_tracks)


def view_all_track_in_playlist():
    print(playlist_options['5'])
    playlist_records = db.all_playlists()
    playlist_empty = utilities.show_all_playlists(playlist_records)
    if playlist_empty:
        return
    playlist_id = utilities.input_type(data_type=int, field='playlist id')
    if playlist_id:
        record = db.playlist_by_id(playlist_id)
        if record:
            show_all_track_and_play(playlist_id)
        else:
            print(f'Playlist not found with ID: {playlist_id}')
    else:
        print('Playlist id takes only integer data value (>0)')


def search_playlists(choose):
    print(playlist_options['6'])
    music_tracks = utilities.search_tracks(choose)
    ids = (int(track.id) for track in music_tracks)
    playlists = db.playlist_by_ids(ids)
    playlist_empty = utilities.show_all_playlists(playlists)
    if playlist_empty:
        return
    playlist_id = utilities.input_type(data_type=int, field='playlist id')
    if playlist_id:
        record = db.playlist_by_id(playlist_id)
        try:
            playlists.index(record)
            if record:
                show_all_track_and_play(playlist_id)
            else:
                print(f'Playlist not found with ID: {playlist_id}')
        except:
            print(f'No playlists with ID {playlist_id} found in playlist search results')
    else:
        print('Playlist id takes only integer data value (>0)')


def main():
    while True:
        utilities.clear_cmd()
        print('Playlist Managment')
        print('\t1. Create new a playlist.')
        print('\t2. Delete playlists')
        print('\t3. Add tracks to playlist.')
        print('\t4. Delete tracks in playlist.')
        print('\t5. Display a list of all playlists.')
        print('\t6. View the details of a specific playlists by searching.')
        print('\t7. Exit')
        input_check = ('1', '2', '3', '4', '5', '6', '7')
        choose = utilities.feature_type_input(input_check)
        if choose == '1':
            utilities.run_feature(add_new_playlist)
        elif choose == '2':
            utilities.run_feature(delete_playlists)
        elif choose == '3':
            utilities.run_feature(add_track_to_playlist)
        elif choose == '4':
            utilities.run_feature(delete_track_in_playlist)
        elif choose == '5':
            utilities.run_feature(view_all_track_in_playlist)
        elif choose == '6':
            utilities.run_feature_search(search_playlists)
        elif choose == '7':
            break
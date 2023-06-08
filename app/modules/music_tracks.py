import db
import utilities
from config import track_options

def add_new_track() -> None:
    print(track_options['1'])
    print('Please enter the required information:')
    status, file_name = utilities.select_file()
    if status:
        title = utilities.input_type(data_type=str, field='title', required=True)
        artist = utilities.input_type(data_type=str, field='artist')
        album = utilities.input_type(data_type=str, field='album')
        genre = utilities.input_type(data_type=str, field='genre')
        release_year = utilities.input_type(data_type=int, field='release year')
        path_key = file_name
        duration = utilities.get_duration(file_name)
        new_record = db.MusicTracks(title=title, artist=artist, album=album, genre=genre, release_year=release_year,
                                    duration=duration, path_key=path_key)
        db.add_record(new_record)
        print('Add new music track success!!')


def delete_tracks() -> None:
    print(track_options['4'])
    music_tracks = db.all_tracks()
    track_empty = utilities.show_all_tracks(music_tracks)
    if track_empty:
        return
    ids = utilities.input_type(data_type=str, field='ids to remove separated by ","')
    ids = ids.split(',')
    if len(ids) > 0:
        for id in ids:
            temp_id = id.strip()
            try:
                record = db.track_by_id(int(temp_id))
                if record:
                    db.delete_record(record)
                    utilities.delete_file(record.path_key)
                    print(f'Deleted music track ID: {temp_id}')
                else:
                    print(f'Music track not found with ID: {temp_id}')
            except:
                print(f'Music track not found with ID: {temp_id}')
        db.record_commit()
    return


def update_track() -> None:
    print(track_options['3'])
    music_tracks = db.all_tracks()
    track_empty = utilities.show_all_tracks(music_tracks)
    if track_empty:
        return
    temp_id = utilities.input_type(data_type=int, field='music track id to update')
    record = db.track_by_id(temp_id)
    if record:
        msg = 'Do you want to change the old audio file?'
        choose = utilities.continue_again(msg=msg)
        if choose.upper() == 'Y':
            status, file_name = utilities.select_file()
            if status:
                utilities.delete_file(record.path_key)
                record.path_key = file_name
                record.duration = utilities.get_duration(file_name)
        record.title = utilities.input_type_default(data_type=str, field='title', value_default=record.title)
        record.artist = utilities.input_type_default(data_type=str, field='artist', value_default=record.artist)
        record.album = utilities.input_type_default(data_type=str, field='album', value_default=record.album)
        record.genre = utilities.input_type_default(data_type=str, field='genre', value_default=record.genre)
        record.release_year = utilities.input_type_default(data_type=int, field='release year', value_default=record.release_year)
        db.record_commit()
        print('Update music track success')
    else:
        print(f'Music track not found with ID: {temp_id}')


def view_all_tracks():
    print(track_options['5'])
    music_tracks = db.all_tracks()
    utilities.show_all_tracks(music_tracks)
    if music_tracks:
        utilities.handle_open_music(music_tracks)


def search_tracks(choose):
    print(track_options['2'])
    music_tracks = utilities.search_tracks(choose)
    utilities.show_all_tracks(music_tracks)
    if music_tracks:
        utilities.handle_open_music(music_tracks)


def main():
    while True:
        utilities.clear_cmd()
        print('Music Tracks Managment')
        print('\t1. Add a new music track.')
        print('\t2. View the details of a specific music track by searching.')
        print('\t3. Update the details of an existing music track.')
        print('\t4. Delete a music track from the library.')
        print('\t5. Display a list of all music tracks in the library.')
        print('\t6. Exit')
        input_check = ('1', '2', '3', '4', '5', '6')
        choose = utilities.feature_type_input(input_check)
        if choose == '1':
            utilities.run_feature(add_new_track)
        elif choose == '2':
            utilities.run_feature_search(search_tracks)
        elif choose == '3':
            utilities.run_feature(update_track)
        elif choose == '4':
            utilities.run_feature(delete_tracks)
        elif choose == '5':
            utilities.run_feature(view_all_tracks)
        elif choose == '6':
            break
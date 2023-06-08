import shutil
import config
import uuid
import os
import tkinter as tk
from tkinter import filedialog
import db
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer


def generate_id() -> str:
    '''initialize id'''
    random_str = str(uuid.uuid4().hex)
    return random_str[:13]


def clear_cmd():
    '''clear cmd'''
    os.system('cls' if os.name == 'nt' else 'clear')


def file_browsing() -> str:
    '''Browse *.mp3 and *.wav audio files on user's computer'''
    print('Please browse your file...')
    root = tk.Tk()
    root.focus()
    root.withdraw()
    filetypes = (
        ('Music files', ['*.mp3', '*.wav']),
        ('All files', '*.*')
    )
    file_path = filedialog.askopenfilename(
        title='Open a file',
        filetypes=filetypes)
    if not file_path:
        print('Failed because the file was not selected')
    return file_path


def copy_file(file_path: str, file_name_copy: str) -> bool:
    '''copy audio files from user's computer to sound library folder'''
    file_name = file_path.split('/')[-1]
    file_format = file_name.split('.')[-1]
    if file_format.endswith('mp3') or file_format.endswith('wav'):
        print(f"Copying {file_name}")
        shutil.copyfile(file_path, f'{config.COPY_DIRECTORY}{file_name_copy}.{file_format}')
        return True
    else:
        print('Failed because the file is not in *.mp3 or *.wav format')
        return False


def delete_file(file_name: str):
    '''delete a file in the saved audio library folder with the provided file name'''
    #print('Deleting file...')
    os.remove(config.COPY_DIRECTORY + file_name)
    #print('Delete file success')


def select_file():
    '''The entire process of saving files to the database when adding or 
    updating files in the database of a music track'''
    file_name_ori = file_browsing()
    if file_name_ori:
        file_name_record = generate_id()
        is_copy_success = copy_file(file_name_ori, file_name_record)
        if is_copy_success:
            file_format = file_name_ori.split('.')[-1]
            file_name_new = f'{file_name_record}.{file_format}'
            return True, file_name_new
        else:
            return False, ''
    else:
        return False, ''


def input_type(data_type, field: str, required: bool=False):
    '''Let the user enter data with data bindings'''
    while True:
        try:
            value = data_type(input(f'Please provide information of {field}: '))
            if required and not value:
                print(f'{field} data value must not be empty')
                continue
            return value
        except:
            print(f'data value only supports {data_type} type')

def input_type_default(data_type, field: str, value_default):
    '''Let the user enter data with data bindings and default values if empty'''
    print('If your input value is empty, the old value will be preserved')
    while True:
        try:
            value = data_type(input(f'Please provide information of {field} ({value_default}): ') or value_default) 
            return value
        except:
            print(f'{field} data value only supports {data_type} type')

def feature_type_input(input_check: set) -> bool:
    '''Let the user choose the feature type if the value is not 
    valid there will be an error message and ask to re-enter'''
    while True:
        choose = input(f'Please select function {input_check}: ')
        if choose.lower().strip() in input_check or choose.upper().strip() in input_check:
            break
        else:
            print('Please choose again because the function code is not valid')

    return choose


def continue_again(msg: str = 'Do you want to do it again?', input_check: set = ('Y', 'N')) -> str:
    '''Ask the user whether to do it again with the feature just done or failed.'''
    print(msg)
    choose = feature_type_input(input_check)
    return choose


def show_all_tracks(records: list):
    '''Show all data of the muisc_tracks table'''
    is_empty = False
    print(f'\n{"*"*135}')
    if records:
        print(f'{"":60s} Music Tracks Table')
        print(
            f"\t{'ID':5s} {'Title':30s} {'Artist':25s} {'Album':20s} {'Genre':12s} {'Release year':15s} {'Duration':5s}")
        for track in records:
            duration_str = format_duration(track.duration)
            print(f"\t{str(track.id):5s} {track.title:30s} {track.artist:25s} {track.album:20s} {track.genre:12s} {str(track.release_year):15s} {duration_str:5s}")
    else:
        print('Can not find any music track')
        is_empty = True
    print(f'{"*"*135}\n')
    return is_empty


def show_all_playlists(records: list):
    '''Show all data of playlists table'''
    is_empty = False
    print(f'\n{"*"*100}')
    if records:
        print(f'{"":8s} Playlists Table')
        print(
            f"\t{'ID':5s} {'Title':20s}")
        for record in records:
            print(f"\t{str(record.id):5s} {record.title:20s} ")
    else:
        is_empty = True
        print('Can not find any playlist')
    print(f'{"*"*100}\n')
    return is_empty


def search_tracks(type_search: str):
    '''Search for music tracks by field entered by user'''
    search_input = input('Please enter the keyword you want to search for: ')
    if type_search == '1':
        music_tracks = db.search_track_details_by_title(search_input)
    elif type_search == '2':
        music_tracks = db.search_track_details_by_artist(search_input)
    elif type_search == '3':
        music_tracks = db.search_track_details_by_album(search_input)
    else:
        music_tracks = db.search_track_details_by_genre(search_input)

    return music_tracks


def run_feature(feature):
    ''''''
    while True:
        clear_cmd()
        feature()
        choose = continue_again()
        if choose.upper() == 'N':
            break
        else:
            continue


def run_feature_search(feature):
    ''''''
    while True:
        clear_cmd()
        print('Choose type search:')
        print('\t1. Search by music track title.')
        print('\t2. Search by music track artist.')
        print('\t3. Search by music track album.')
        print('\t4. Search by music track genre.')
        print('\t5. Exit')
        input_check = ('1', '2', '3', '4', '5')
        choose = feature_type_input(input_check)
        if choose == '5':
            break
        feature(choose)
        choose = continue_again()
        if choose.upper() == 'N':
            break
        else:
            continue


def init_obj_music():
    '''initialize the mixer module'''
    mixer.init()
    

def cancel_obj_music():
    '''uninitialize the mixer'''
    mixer.quit()


def get_duration(file_name):
    '''get duration from file mp3'''
    init_obj_music()
    file = mixer.Sound(config.COPY_DIRECTORY + file_name)
    duration = int(file.get_length())
    cancel_obj_music()
    return duration

def format_duration(time):
    '''format duration to format hour:minute:second'''
    second = time % 60
    if second < 10:
        second = f'0{second}'
    minute = time // 60
    if minute > 60:
        hour = minute // 60
        minute = minute % 60
        if minute < 10:
            minute = f'0{minute}'
        if hour < 10:
            hour = f'0{hour}'
        duration = f'{hour}:{minute}:{second}'
    else:
        if minute < 10:
            minute = f'0{minute}'
        
        duration = f'{minute}:{second}'
        
    return duration

def play_music(record):
    '''
    1. Load a music file for playback
    2. set the music volume
    3. Start the playback of the music stream
    '''
    mixer.music.load(config.COPY_DIRECTORY + record.path_key)
    mixer.music.set_volume(1)
    mixer.music.play()
    print(f'\tMusic "{record.title}" is playing')

def pause_music(record):
    '''temporarily stop music playback'''
    mixer.music.pause()
    print(f'\tMusic "{record.title}" Paused')
    return True

def unpause_music():
    '''resume paused music'''
    mixer.music.unpause()
    return False

def stop_music(record):
    '''stop the music playback'''
    mixer.music.stop()
    print(f'\tMusic "{record.title}" stopped')
    
def check_music_playing():
    '''check if the music stream is playing'''
    result = mixer.music.get_busy()
    return result

def play_music_by_id(records):
    '''Play music according to the user's entered track id'''
    play_again = False
    track_id = input_type(data_type=int, field='music track id to play', required=True)
    record = db.track_by_id(track_id)
    if record:
        try:
            index_record = records.index(record)
            play_again = action_music(records, index_record)
        except:
            print(f'Music track not found with ID: {track_id} in list')
    else:
        print(f'Music track not found with ID: {track_id}')
    if play_again:
        play_music_by_id(records=records)


def index_handle_previous(curr_index, last_index):
    ''''''
    if curr_index == 0:
        curr_index = last_index
    else:
        curr_index -= 1
    
    return curr_index


def index_handle_next(curr_index, last_index):
    ''''''
    if curr_index == last_index:
        curr_index = 0
    else:
        curr_index += 1
    
    return curr_index



def action_music(records, index_record):
    '''Handle actions while playing a track'''
    curr_music = records[index_record]
    curr_index = index_record
    last_index = len(records) - 1
    init_obj_music()
    print('\t1. Pause music')
    print('\t2. Resume paused music')
    print('\t3. Previous music')
    print('\t4. Next music')
    print('\t5. Stop music')
    print('\t6. Play music track by track id')
    play_music(curr_music)
    pause_status = False
    while True:
        input_check = ('1', '2', '3', '4', '5', '6')
        choose = feature_type_input(input_check)
        if not pause_status and choose == '1':
            pause_status  = pause_music(curr_music)
        elif pause_status and choose == '2':
            pause_status = unpause_music()
        elif choose == '3':
            curr_index = index_handle_previous(curr_index, last_index)
            stop_music(curr_music)
            curr_music = records[curr_index]
            play_music(curr_music)
        elif choose == '4':
            curr_index = index_handle_next(curr_index, last_index)
            stop_music(curr_music)
            curr_music = records[curr_index]
            play_music(curr_music)
        elif choose == '5':
            stop_music(curr_music)
            break
        elif choose == '6':
            stop_music(curr_music)
            return True


def handle_open_music(music_tracks):
    '''The entire execution of opening a track'''
    choose = continue_again(msg='Would you like to listen to a track from the displayed list?')
    if choose.upper() == 'Y':
        play_music_by_id(music_tracks)
from modules.music_tracks import main as music_tracks_management
from modules.playlists import main as playlist_management
import utilities


def main():
    while True:
        utilities.clear_cmd()
        print('*'*80)
        print(f'{"":20s}{"Music Library Management System"}')
        print('*'*80)
        print('\t1. Music Tracks Managment')
        print('\t2. Playlists Managment')
        print('\t3. Exit')
        print('*'*80)
        print('\n')
        input_check = ('1', '2', '3')
        choose = utilities.feature_type_input(input_check)
        if choose == '1':
            music_tracks_management()
        elif choose == '2':
            playlist_management()
        elif choose == '3':
            print('Closing the app...')
            break


if __name__ == '__main__':
    main()

#change
HOST_DB = '127.0.0.1' #IP of MySQL server
PORT_DB = '3306' #PORT of MySQL server
NAME_DB = 'music_library_management' #schema name
USER_DB = 'root' #the user account can access that schema (user)
PASSWORD_DB = 'hoangdat77ct' #the user account can access that schema (password)

#no change
DATABASE_URI = f'mysql+pymysql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}'

#may change
COPY_DIRECTORY = './Tracks/'

#no change
track_options = {
    '1': 'Add a new music track.',
    '2': 'View the details of a specific music track by searching.',
    '3': 'Update the details of an existing music track.',
    '4': 'Delete a music track from the library.',
    '5': 'Display a list of all music tracks in the library.',
    '6': 'Exit'
}
#no change
playlist_options = {
    '1': 'Create new a playlist.',
    '2': 'Delete playlists',
    '3': 'Add tracks to playlist.',
    '4': 'Delete tracks in playlist.',
    '5': 'Display a list of all playlists.',
    '6': 'View the details of a specific playlists by searching.',
    '7': 'Exit'
}



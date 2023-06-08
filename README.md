# Music-Library-Management-System
A music library management system with a command-line interface. The system should allow users to organize and manage their music collection (tracks and playlists) by providing various features to add, update, search, and delete entries.
# Directory structure:
- Tracks folder: Save the saved track files in the database.
- config.py: Stores database and program configuration variables
- main.py: File to run the program
- db.py: A file that stores the classes (models) and query functions of the database
- Modules folder: Contains the program's modules (music track and playlist)
  - music_tracks.py: Functions that execute the features of music track management
  - playlists.py: Functions that execute the features of playlist management
# Install environment:
- Python version: > 3.6 (Recomend 3.8.8)
- OS: Windows 10 Home (Tested OS)
- Database MySQL: You need to install a MySQL server first
  - Create new schema. Then import the .sql file to your server. (database folder)
  - Then change the configuration parameters according to your database server in the config.py file
  like "HOST_DB", "PORT_DB", "NAME_DB", "USER_DB", "PASSWORD_DB"
- Virtual environment (Optional):
  - Create Virtual environment: 
    + python -m venv path_to_myenv
  - Navigate to the path containing the newly created virtual environment folder: 
    + cd path_contains_myenv
  - For Windows: 
    + myenv_name\Scripts\activate
  - For Linux: 
    + source venv/bin/activate
- After activating the virtual environment, install: the necessary libraries for the program
  - pip install -r requirements.txt
- Run the program:
  - python main.py
# Instructions on how to use:
- After running the program, there will be 3 options in order including: music track management, playlist management and exit. 
- You need to enter the sequence number to access the functions if the order number is wrong you will have to re-enter it.
- For music track management, there will be 5 functions including:
  1. Add a new music track.
  2. View the details of a specific music track by searching.
  3. Update the details of an existing music track.
  4. Delete a music track from the library.
  5. Display a list of all music tracks in the library.
- For playlist management, there will be 6 functions including:
  1. Create new a playlist..
  2. Delete playlists.
  3. Add tracks to playlist.
  4. Delete tracks in playlist.
  5. Display a list of all playlists.
  6. View the details of a specific playlists by searching.
- Note: After selecting the functions, the program will ask you to enter the information if you enter the wrong or wrong data type, there will be a message and you will have to enter it again. In addition, functions 2, 5 (music management) and functions 5, 6 (playlist management) after searching and displaying the track list you can directly listen to a track with the track ID you provided.
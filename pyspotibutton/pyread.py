import serial
import os
import time
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

serial_port = "/dev/ttyUSB0"

#begin authentication section

req_scopes = "user-library-read user-read-currently-playing user-library-modify"
#user-library-read is for "Check User's Saved Tracks"
#user-read-currently-playing is for "Get Currently Playing Track"
#user-library-modify is for Save Tracks for Current User

#server app information
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
redirect_uri = "http://localhost/"

#creating object for spotipy named spotify_query
#spotify query uses authentication method provided by the spotipy library to get an access token to use for future spotify api requests
spotify_query = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, scope=req_scopes, redirect_uri=redirect_uri))

arduino = serial.Serial(serial_port, 9600, timeout=1)

while True: #looping starting hear
    serialData = ' '
    serialValue = ' '
    bytesWaiting = arduino.in_waiting # updates the num of bytes waiting in buffer
    if bytesWaiting > 0: # if there is something in buffer
        serialData = arduino.read() #update serialData to raw serial data and clear buffer
        serialValue = serialData.decode('UTF-8') # decode to a python friendly string
        if serialValue == 'B': # check if input value is B (begin)
            currentTrack = spotify_query.current_user_playing_track() #current track now contains all info about current spotify usage
            if currentTrack == None: #if there is not a current track
                arduino.write(str.encode('N')) #signal to arduino that there is no track playing
            else:
                isPlaying = currentTrack['is_playing']
                if isPlaying == False: #if paused
                    arduino.write(str.encode('N')) #signal to arduino that track is paused
                else:
                    isPlayingID = [currentTrack['item']['id']]
                    isSaved = spotify_query.current_user_saved_tracks_contains(tracks=isPlayingID)
                    if isSaved == [False]:
                        arduino.write(str.encode('W')) # song is not saved, so it Will be saved
                        spotify_query.current_user_saved_tracks_add(tracks=isPlayingID)
                    else:
                        arduino.write(str.encode('A'))



            


# currentTrack = spotify_query.current_user_playing_track() #is playing will contain None if nothing is playing, and a JSON file if they are
# if currentTrack == None: #if there is a current track
#     arduino.write(str.encode("0"))
#     print(arduino.readline().decode('ascii'))
#     #print("Nothing is Playing")
# else:
#     isPlayingid = [currentTrack['item']['id']] #tracks parameter needs to be a list hence the use of []
#     isSaved = spotify_query.current_user_saved_tracks_contains(tracks=isPlayingid)
#     if isSaved == [False]:
#         arduino.write(str.encode("2"))
#         print(arduino.readline().decode('ascii'))
#         #print("you dont have this song liked")
#     else:
#         arduino.write(str.encode("1"))
#         print(arduino.readline().decode('ascii'))
#         #print("you do have this song liked")

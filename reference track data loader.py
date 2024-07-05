# Ryder Katz
#
# This program uses spotify's api to load reference tracks to a file within the program folder
#
# In order for the program to work, the user must have:
#       spotipy
#       a spotify developer client ID and client secret
#       'filePath' adjusted to the path on the user's computer to the 'Reference Song Data.txt' file
#



# this program makes use of the spotipy python library for handling the spotify api data
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# this is the path to the file where the api data will be stored
filePath = '/Users/ryderkatz/Documents/Python Projects/Reference Track Finder Program/Reference Song Data.txt'


# connects to spotify api
cid = ''    # enter spotify developer client ID here
secret = ''     # enter spotify developer client secret here
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager =
client_credentials_manager)


# this is the spotify URI of the playlist you intend to grab song features from
# spotify api will only analyze the first 100 songs in any given playlist
# you can replace this URI with different playlists and run the program again to add more data
# repeats will be checked for, so the song data file will only add new songs 
playlistID = '37i9dQZF1DXcBWIGoYBM5M'
    # the playlist ID is currently set to Spotify's Today's Top Hits playlist, as an example



# this function takes the spotify playlist and gets the basic track data
# the data is returned as a set of tuples
def gatherFromPlaylist(playlist_id, numberTracks):
    #
    # parameter 'playlist_id' is the URI to a spotify playlist
    # paramter 'numberTracks' is the amount of tracks you want to analyze
    # if the number of tracks to be analyzed is more than 100, only 100 will be processed
    #
    playlistTracks = set()
    for track in sp.playlist_tracks(playlist_id, limit=numberTracks)["items"]:
        track_id = track["track"]["id"]
        track_name = track["track"]["name"]
        track_artist = track["track"]["album"]["artists"][0]["name"]
        playlistTracks.add((track_id, track_name, track_artist))
    print(f'{len(playlistTracks)} tracks gathered')
    return playlistTracks


# this function takes the basic track data and gathers various track features
# the data is returned as a set of tuples
def getFeatures(tracks):
    #
    # parameter 'tracks' is a set of tuples
    # those tuples are formatted as (track_id, track_name, track_artist)
    #
    trackFeatures = set()
    for track_id, trackName, trackArtist in tracks:
        
        features = sp.audio_features(track_id)[0]
        features = dict(features)

        key = features["key"]  #int
        tempo = features["tempo"]  #float
        loudness = features["loudness"]  #float
        valence = features["valence"] #0.0-1.0 with more positive songs having higher valence
        energy = features["energy"] # 0.0-1.0 with higher energy being louder, faster, noisier
        danceability = features["danceability"] # 1.0 is maximum danceability

        trackFeatures.add((trackName, key, tempo, loudness, energy, danceability, valence, trackArtist, track_id))
    return trackFeatures



# this function checks the songs already in the file to avoid adding repeats
# it then adds the data for the new unique songs
def addTracks_existingFile(filePath, trackFeatures):
        with open(filePath, 'r') as file:
            data = file.readlines()
        songCount = 0
        for track in trackFeatures:
            repeatCount = 0
            for line in data:
                split = line.split(',,')
                if split[0] == str(track[0]):
                    repeatCount += 1
            if repeatCount < 1:
                with open(filePath,'a') as file:
                    track_data = ',,'.join(str(value) for value in track) + '\n'
                    file.write(track_data)
                    songCount += 1
        print(f'{songCount} songs added')



# this function only runs when there is no data in the file (the first time the program is ran)
# it adds the data without checking for repeats
def addTracks_emptyFile(filePath, trackFeatures):
    with open(filePath, 'a') as file:
        for track in trackFeatures:
            track_data = ',,'.join(str(value) for value in track) + '\n'
            file.write(track_data)



# this function adds the track data to the file, using one of the two functions defined directly above
def addTracks(filePath, trackFeatures):
    newFileNeeded = False
    try:
        addTracks_existingFile(filePath,trackFeatures)
    except:
        print('Starting new file')
        newFileNeeded = True
    if newFileNeeded:
        addTracks_emptyFile(filePath, trackFeatures)





# this line will call the functions above to run the program
addTracks(filePath, getFeatures(gatherFromPlaylist(playlistID,100)))
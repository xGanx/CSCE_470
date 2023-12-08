"""
Come Back to Later:
https://pypi.org/project/forceatlas2py/
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679

TODO:
 * Implement force graph visualiziation with realtime adjustments to parameters used for determining centroids to determine best features to use to make recommendations with
 * Add data to postgres database
 * Seperate script into multiple different scripts, one for populating database, another for making recommendations based on info in database
 *
 
Notes:
 * Breakcore and Chill playlists are absorbing most of the recommendations currently
 * The Sick! playlist (metalcore) seems to be hard to classify under the current supported features
"""

import sys
import os
from dotenv import load_dotenv
load_dotenv()

import numpy as np

import json

import time
requests_per_second = 1

# import logging
# logger = logging.getLogger('parser.py')
# logging.basicConfig(level='DEBUG')

import spotipy
from spotipy.oauth2 import SpotifyOAuth

auth_manager = SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                            client_secret=os.getenv("CLIENT_SECRET"),
                            redirect_uri='http://localhost:3000',
                            scope='user-library-read playlist-modify-public')


sp_client = spotipy.Spotify(auth_manager=auth_manager)

"""
    Danceability: takes into account tempo, rhythm stabilty, beat strength, and overall regularity to described how suitable a track is to dance to
    Energy: a perceptual measure of intensity and activity
    Loudness: overall loudness of track in decibels averaged across the track
    Speechiness: presence of words in track
    Acousticness: tanks into
    Instrumentalness: =predicts whether a track contains no vocals
    Valence: describes musical positiveness  (high valence = happy cheerful euphoric, low valence = sad dperessed angry)
    Tempo: beats per minute
    Key: key of the track, uses pitch class notation
"""

features_to_get = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','valence','tempo', 'key']

jsonDump = open('jsonDump.json','w')

def testUserSpecificFunctionality():
    results = sp_client.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " - ", track['name'])
        
def getUserPlaylists():
    user_playlists = []
    
    cursor=0
    total = 0
    
    count = 0
    
    while True:
        try:
            results = sp_client.current_user_playlists(limit=50, offset=cursor)
            jsonDump.write(json.dumps(results, indent=4))
        except spotipy.client.SpotifyException as err:
            print(err)
            sys.exit(1)
        total = results['total']
        
        # print(results)
        
        for _, item in enumerate(results['items']):
            count += 1
            print("%d %s" % (count, item['name']))
            
            user_playlists.append((item['name'],item['id']))
            
        cursor += 50
        if cursor > total:
            return user_playlists
    
    return user_playlists
        
def getPlaylistSongs(playlist_id):
    songs = []
    
    try:
        results = sp_client.playlist_tracks(playlist_id=playlist_id)
        jsonDump.write(json.dumps(results, indent=4))
    except spotipy.client.SpotifyException as err:
            print(err)
            sys.exit(1)
    
    # print(json.dumps(results, indent=4))
    
    # print(results['items'])
    
    tracks = results['items']
    
    for track in tracks:
        # print((track['track']['name'],track['track']['id']))
        if track['track']['id'] is None:
            continue
        songs.append((track['track']['name'],track['track']['id']))
    
    return songs

def getSongFeatures(song_name, song_id):
    global features_to_get
    
    print(f'Getting the features for {song_name}...')
    
    try:
        response = sp_client.audio_features((song_id))
        jsonDump.write(json.dumps(response, indent=4))
    except spotipy.client.SpotifyException as err:
            print(err)
            sys.exit(1)
    
    features = dict()
    for feature in features_to_get:
        features[feature] = response[0][feature]
    
    # print(response)
    
    # print(features)
    
    return features

def generateKCluster(songs):
    return

def rocchioSimilarity():
    return

def getKNearestCluster():
    return

def addSongToPlaylist(playlist_id, song_id, playlist_name, song_name):
    print(f'Adding {song_name} to the playlist {playlist_name}...')
    
    print(f'Playlist id = {playlist_id} | Song id = {song_id}')
    
    try:
        sp_client.playlist_add_items(playlist_id=playlist_id,items=[song_id])
    except spotipy.client.SpotifyException as err:
            print(err)
            sys.exit(1)
    return
 
def addSongListToPlaylist(playlist_id, playlist_name, song_list):
    
    for song_name, song_id in song_list:
        print(f'Adding {song_name} to the playlist {playlist_name}...')
    
        try:
            sp_client.playlist_add_items(playlist_id=playlist_id,items=[song_id])
        except spotipy.client.SpotifyException as err:
            print(err)
            sys.exit(1)
    return


def main():
    print("Running spotify parsing script")
    
    # Sanity check test
    # testUserSpecificFunctionality()
    
    # get playlist name + id as tuple pairs
    user_playlists = getUserPlaylists() # (playlist_name, id)

    # Flavor of the Week = 2
    parse_playlist = input('Enter number of playlist you want to parse >>> ')
    playlist_to_sort = user_playlists[int(parse_playlist)-1]
    
    # print(playlist_to_sort)
    # return
    
    # Playlists to Parse Into = 1 6 13 19 25 27 28 29 30
    '''
    Playlist 2: Flavor of the Year (2023)
    
    Playlist 1: Climbing
    Playlist 6: Breakcore
    Playlist 13: Electronic
    Playlist 19: Sick (metalcore playlist)
    Playlist 25: Chill (in rock folder)
    Playlist 27: ...
    Playlist 28: Kpop
    Playlist 29: Weeb
    Playlist 30: R&B
    '''
    parse_into_playlists_input = input('Enter number of playlists you want to parse song into (separate numbers by spaces) >>> ')
    
    playlist_name_id_dict = dict()
    
    parse_into_playlists = []
    for playlist_num in parse_into_playlists_input.split():
        parse_into_playlists.append(user_playlists[int(playlist_num)-1])
    
    # print(user_playlists)
    
    # print(parse_playlist)
    # print(parse_into_playlists)
    
    print('Parsing playlists...')
    
    # Get songs for a playlist:
    # songs = getPlaylistSongs(parse_into_playlists[0][1])
    
    # testing if add to playlist works - works
    # addSongToPlaylist(parse_into_playlists[0][1], songs[0][1], parse_into_playlists[0][0], songs[0][0])
    
    # Get features of a song
    # features = getSongFeatures(songs[0][0], songs[0][1])
    
    # <----------------------------------- Main Code ----------------------------------->
    # Generate all clusters (hopefully clusters) from the songs in each playlist being parsed into
    centroids = []
    
    for playlist_name, playlist_id in parse_into_playlists:
        playlist_name_id_dict[playlist_name] = playlist_id
        
        # time.sleep(1 / requests_per_second)
        songs = getPlaylistSongs(playlist_id)
        
        features = []
        for song_name, song_id in songs:
            features.append(getSongFeatures(song_name, song_id))
            
        # print(features)
        
        data_array = np.array([[point[attr] for attr in point] for point in features])
        
        print('Data Array 1: ', data_array)
        
        centroid = np.mean(data_array, axis=0)
        
        print(f'Centroid: {centroid}')
        
        centroids.append({playlist_name: centroid})
        
        time.sleep(5)
    
    print(centroids)
    
    # Parse through the given input playlist and start making playlist recommendations for each song
    # This uses Rocchio classification
    input_songs = getPlaylistSongs(playlist_to_sort[1])
    
    for song_name, song_id in input_songs:
        input_features = [getSongFeatures(song_name, song_id)]
            
        new_song = np.array([[point[attr] for attr in point] for point in input_features])
        
        # Calculate Rocchio Distance between the song and each centroid
        rocchio_distances = []
        for centroid in centroids:
            for playlist_name, value in centroid.items():
                rocchio_distance = np.linalg.norm(value - new_song)
                rocchio_distances.append((playlist_name, rocchio_distance))
        
        # Sort to find minimum rocchio distance
        rocchio_distances.sort(key=lambda x: x[1])
        
        # Display the closest centroid
        closest_centroid = rocchio_distances[0]
        
        # show order of centroids
        for rocchi_dist, playlist_name in rocchio_distances:
            print(f'Playlist: {playlist_name}, Rocchio Distance: {rocchi_dist}')
        print()
        
        print(f'The song {song_name} is most similar to the playlist {closest_centroid[0]}')
        
        addSong = input('Do you want to add the song to the playlist (y or n) >>> ')
        
        if addSong == 'y':
            addSongToPlaylist(playlist_name_id_dict[closest_centroid[0]], song_id, closest_centroid[0], song_name)
    
    jsonDump.close()

if __name__ == "__main__":
    main()
    
    
    
# use k nearest neighbors and then rocchio classification (nearest centroid classificaiton)
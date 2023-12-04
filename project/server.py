import os
from dotenv import load_dotenv
load_dotenv()

import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyOAuth

auth_manager = SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                        client_secret=os.getenv("CLIENT_SECRET"),
                                        redirect_uri='http://localhost:3000',
                                        scope='user-library-read')


sp_client = spotipy.Spotify(auth_manager=auth_manager)

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
        results = sp_client.current_user_playlists(limit=50, offset=cursor)
        total = results['total']
        
        #print(results)
        
        for _, item in enumerate(results['items']):
            count += 1
            print("%d %s" % (count, item['name']))
            
            user_playlists.append(item['name'])
            
        cursor += 50
        if cursor > total:
            return user_playlists
    
    return user_playlists
        
def getPlaylistSongs(playlist):
    return

def generateKCluster(songs):
    return

def rocchioSimilarity():
    return

def getKNearestCluster():
    return

def addSongToPlaylist(song, playlist):
    return


def main():
    print("Running spotify parsing script")
    
    # Sanity check test
    # testUserSpecificFunctionality()
    
    user_playlists = getUserPlaylists()

    # Flavor of the Week = 2
    parse_playlist = input('Enter number of playlist you want to parse >>> ')
    
    # Playlists to Parse Into = 1 6 18 19 25 27 28 29 30
    parse_into_playlists_input = input('Enter number of playlists you want to parse song into (separate numbers by spaces) >>> ')
    
    parse_into_playlists = parse_into_playlists_input.split()
    
    print(user_playlists)
    
    print(parse_playlist)
    print(parse_into_playlists)

if __name__ == "__main__":
    main()
    
    
    
# use k nearest neighbors and then rocchio classification (nearest centroid classificaiton)
"""
Come Back to Later:
https://pypi.org/project/forceatlas2py/
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679
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

def addSongToPlaylist(playlist_id, song_id, playlist_name, song_name):
    print(f'Adding {song_name} to the playlist {playlist_name}...')
    
    print(f'Playlist id = {playlist_id} | Song id = {song_id}')
    
    try:
        sp_client.playlist_add_items(playlist_id=playlist_id,items=[song_id])
    except spotipy.client.SpotifyException as err:
            print(err)
            sys.exit(1)
    return

addSongToPlaylist('','','','')
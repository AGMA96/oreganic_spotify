import json
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

INPUT_PATH = os.path.normpath(os.path.join(os.getcwd(),'..', 'input', 'liked_artists_ids.json'))

with open(INPUT_PATH, 'r', encoding='utf-8') as artists_file:
    artists = json.load(artists_file)

    for id, name in artists.items():
        print("{} {}".format(id, name))
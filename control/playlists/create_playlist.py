import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
import json

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# variables
playlist_name = 'new releases'
playlist_description = 'new releases from all countries'
#

created_playlist = sp.user_playlist_create(
    user='jmnbnouc9pwqvey53cawle9jy',
    name=playlist_name,
    description=playlist_description,
    public=False)

with open(os.path.join(os.getcwd(), created_playlist['id'] + '.json'), 'w', encoding='utf-8') as created_playlist_file:
    json.dump(created_playlist, created_playlist_file, indent=4, ensure_ascii=False)

print('new playlist created! : ', created_playlist['name'])
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json
import os
import glob
import time

LIKED_ARTISTS_PATH = os.path.normpath(os.path.join(os.getcwd(), 'jsons', 'Artists', 'input', 'liked_artists_ids.json'))

liked_artists = {}
with open(LIKED_ARTISTS_PATH, 'r', encoding='utf-8') as artists_file:
    liked_artists = json.load(artists_file)
print('liked artists : ', str(len(liked_artists)))

RELATED_ARTISTS_PATHS = glob.glob(os.path.join(os.getcwd(),  'jsons', 'Artists', 'GetArtistsRelatedArtists', '*.json'))
acquired_artists = {os.path.splitext(os.path.basename(path))[0] for path in RELATED_ARTISTS_PATHS}
print('acquired artists : ', str(len(acquired_artists)))

# got related artist from before excuted
related_artists = {}
for related_artists_path in RELATED_ARTISTS_PATHS:
    with open(related_artists_path, 'r', encoding='utf-8') as related_artists_file:
        acquired_artists_json = json.load(related_artists_file)

        for artist in acquired_artists_json['artists']:
            related_artists[artist['id']] = artist['name']

print('related artists : ', str(len(related_artists)))

# 取得済みのアーティストIDを差し引く

target_artists = {k: v for k, v in liked_artists.items() if k not in acquired_artists}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

for artist_id in target_artists.keys():
    related_artists = sp.artist_related_artists(artist_id)

    with open(os.path.join(os.getcwd(), 'jsons', 'Artists', 'GetArtistsRelatedArtists', artist_id + '.json'), 'w', encoding='utf-8') as related_artists_file:
        json.dump(related_artists, related_artists_file, indent=4, ensure_ascii=False)

    time.sleep(1)

    


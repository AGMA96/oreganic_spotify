import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json
import os
import glob
import time

ALBUMS_IDS_PATH = r'xxx\jsons\Albums\input\new_release_albums_ids.json'

albums = {}
with open(ALBUMS_IDS_PATH, 'r', encoding='utf-8') as albums_ids_file:
    albums = json.load(albums_ids_file)
print('albums ids : ', str(len(albums)))

ALBUM_TRACKS_PATHS = glob.glob(os.path.join(os.getcwd(), '*.json'))
acquired_album_tracks = {os.path.splitext(os.path.basename(path))[0] for path in ALBUM_TRACKS_PATHS}
print('acquired albums : ', str(len(acquired_album_tracks)))

# 取得済みのアーティストIDを差し引く

target_albums = {id: name for id, name in albums.items() if id not in acquired_album_tracks}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

for album_id in target_albums.keys():
    try:
        album_tracks = sp.album_tracks(album_id=album_id, market='JP')

        with open(os.path.join(os.getcwd(), album_id + '.json'), 'w', encoding='utf-8') as album_tracks_file:
            json.dump(album_tracks, album_tracks_file, indent=4, ensure_ascii=False)

        time.sleep(1)
    except Exception as e:
        print(e)


    


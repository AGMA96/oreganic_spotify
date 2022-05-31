import json
import os
import glob
import time

from control.client import HeadlessAuth

RELATED_ARTISTS_PATH = os.path.normpath(os.path.join(os.getcwd(),'jsons', 'Artists', 'input', 'related_artists_ids.json'))

related_artists = {}
with open(RELATED_ARTISTS_PATH, 'r', encoding='utf-8') as artists_file:
    related_artists = json.load(artists_file)
print('related artists : ', str(len(related_artists)))

# API実行済みのID(既存のjson名)一覧を取得する
ACQUIRED_PATHS = glob.glob(os.path.join(os.getcwd(), '*.json'))
acquired_artists_ids = {os.path.splitext(os.path.basename(path))[0] for path in ACQUIRED_PATHS}
print('acquired artists : ', str(len(acquired_artists_ids)))

# 取得済みのアーティストIDを差し引く
target_artists = {id: name for id, name in related_artists.items() if id not in acquired_artists_ids}

sp = HeadlessAuth().create_spotipy_client()

for artist_id in target_artists.keys():
    top_tracks = sp.artist_top_tracks(artist_id=artist_id, country="JP")

    with open(os.path.join(os.getcwd(), 'jsons', 'Artists', 'GetArtistsTopTracks', artist_id + '.json'), 'w', encoding='utf-8') as artist_top_tracks_file:
        json.dump(top_tracks, artist_top_tracks_file, indent=4, ensure_ascii=False)

    time.sleep(1)

    


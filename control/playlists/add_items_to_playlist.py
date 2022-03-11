import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json
import os
import glob
import time

def split_list(list):
    length = 100
    for idx in range(0, len(list), length):
        yield list[idx:idx + length]

top_tracks = {}

## variables #
tracks_ids_file_name = 'new_releases_tracks_ids'
playlist_id = '00XAPpcIZVmq5Urym5AQIR'
############# 

TRACKS_PATH = os.path.normpath(os.path.join(os.getcwd(),'..', '..', 'Tracks', 'input', tracks_ids_file_name +'.json'))
with open(TRACKS_PATH, 'r', encoding='utf-8') as tracks_file:
    top_tracks = json.load(tracks_file)
print('artists top tracks: ', str(len(top_tracks)))

ADDED_TRACKS_PATHS = glob.glob(os.path.join(os.getcwd(), '..', 'output', '*.json'))
# TODO JSON構造化 1000曲/1ファイル
'''
[file_name] = 'playlist_id'.json
{
    "items":[
        {
            "snapshot_id": 'snapshot_id',
            "tracks": [
                {
                    "id": 'track_id'
                },
                {
                    ...
                }
            ]
        }
        {
            ...
        }
        }
        {
            ...
        }
    ]
}
'''

# got added tracks from before excuted
added_tracks_before = set()
for related_artists_path in ADDED_TRACKS_PATHS:
    with open(related_artists_path, 'r', encoding='utf-8') as added_tracks_file:
        added_tracks_json = json.load(added_tracks_file)
    for items in added_tracks_json['items']:
        tracks_ids_file_name = {track['id'] for track in items['tracks']}
        added_tracks_before.update(tracks_ids_file_name)

print('already added tracks : ', str(len(added_tracks_before)))

# 追加済みのトラックIDを差し引く
target_tracks = {id: name for id, name in top_tracks.items() if id not in added_tracks_before}

scope="playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

added_tracks = {}
added_tracks['items'] = []

splited_track_list = list(split_list(list(target_tracks.keys())))
for track_list in splited_track_list[:10]: # add only 1,000 tracks

    response = sp.playlist_add_items(playlist_id=playlist_id, items=track_list)
 
    item = {}
    item['snapshot_id'] = response['snapshot_id']
    item['tracks'] = [{'id': track_id} for track_id in track_list]
    added_tracks['items'].append(item)

    print('added tracks(snapshot_id): ', response['snapshot_id'])

    with open(os.path.join(os.getcwd(), response['snapshot_id'] + '.json'), 'w', encoding='utf-8') as response_file:
        json.dump(response, response_file, indent=4, ensure_ascii=False)
        print('dumped! response : ',response_file)
 
    time.sleep(1)

with open(os.path.join(os.getcwd(), '..', 'output', playlist_id + '.json'), 'w', encoding='utf-8') as added_tracks_file:
    json.dump(added_tracks, added_tracks_file, indent=4, ensure_ascii=False)
    print('dumped! ',added_tracks_file)
   

    


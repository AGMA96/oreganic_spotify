import json
import os
import glob

liked_tracks_path_pattern = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'GetUsersSavedTracks', '2022-03-08', '*.json')

tracks_ids = set()

liked_tracks_paths = glob.glob(liked_tracks_path_pattern)
for liked_tracks_path in liked_tracks_paths:
    with open(liked_tracks_path, 'r', encoding='utf-8') as f:
        spotify_json = json.load(f)
    liked_tracks = spotify_json['items']

    for liked_track in liked_tracks:
        tracks_ids.add(liked_track['track']['id'])


print("the number of the tracks : {}".format(len(tracks_ids)))

OUTPUT_PATH = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'input', 'liked_tracks_ids.json')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as tracks_ids_file:
    json.dump(list(tracks_ids), tracks_ids_file, indent=4, ensure_ascii=False)
    print('dumped!')

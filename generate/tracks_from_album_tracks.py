import json
import os
import glob

input_directory = os.path.join(os.getcwd(), 'jsons', 'Albums', 'GetAlbumTracks')

tracks = {}

albums_tracks_files = glob.glob(input_directory + "/*.json")
for file in albums_tracks_files:
    with open(file, 'r', encoding='utf-8') as f:
        spotify_json = json.load(f)
    for track in spotify_json['items']:
        tracks[track['id']] = track['name']



print("the number of the tracks : {}".format(len(tracks)))

OUTPUT_PATH = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'input', 'new_releases_tracks_ids.json')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as tracks_ids:
    json.dump(tracks, tracks_ids, indent=4, ensure_ascii=False)
    print('dumped!')

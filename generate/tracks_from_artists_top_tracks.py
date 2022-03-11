import json
import argparse
import glob

parser = argparse.ArgumentParser(description="get tracks' ids list from json file")
parser.add_argument('-i', '--input_directory')
args = parser.parse_args()

print("input:" + args.input_directory)

tracks = {}

artists_top_tracks_files = glob.glob(args.input_directory+ "/*.json")
for file in artists_top_tracks_files:
    with open(file, 'r', encoding='utf-8') as f:
        spotify_json = json.load(f)
    for track in spotify_json['tracks']:
        tracks[track['id']] = track['name']



print("the number of the tracks : {}".format(len(tracks)))

OUTPUT_PATH = r'xxx\jsons\Tracks\input\artists_top_tracks_ids.json'

with open(OUTPUT_PATH, 'w', encoding='utf-8') as tracks_ids:
    json.dump(tracks, tracks_ids, indent=4, ensure_ascii=False)
    print('dumped!')

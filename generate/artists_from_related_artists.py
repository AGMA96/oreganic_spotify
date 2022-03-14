import json
import argparse
import glob
import os

parser = argparse.ArgumentParser(description="get artists' ids list from json file")
parser.add_argument('-i', '--input_directory')
args = parser.parse_args()

print("input:" + args.input_directory)

artists = {}

related_artists_files = glob.glob(args.input_directory+ "/*.json")
for file in related_artists_files:
    with open(file, 'r', encoding='utf-8') as f:
        spotify_json = json.load(f)
    for artist in spotify_json['artists']:
        artists[artist['id']] = artist['name']



print("the number of the artists : {}".format(len(artists)))

OUTPUT_PATH = os.path.join(os.getcwd(), 'jsons', 'input', 'CreatePlaylist', 'related_artists_ids.json')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as artists_ids:
    json.dump(artists, artists_ids, indent=4, ensure_ascii=False)
    print('dumped!')

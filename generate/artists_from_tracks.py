import json
import argparse
import glob

parser = argparse.ArgumentParser(description="get artists' ids list from json file")
parser.add_argument('-i', '--input_directory')
args = parser.parse_args()

print("input:" + args.input_directory)

artists = {}

liked_tracks_files = glob.glob(args.input_directory+ "/*.json")
for file in liked_tracks_files:
    with open(file, 'r', encoding='utf-8') as f:
        spotify_json = json.load(f)
        liked_songs = spotify_json['items']

        for liked_song in liked_songs:
            for artist in liked_song['track']['artists']:
                artists[artist['id']] = artist['name']



print("the number of the artists : {}".format(len(artists)))

OUTPUT_PATH = r'xxx\jsons\Artists\input\liked_artists_ids.json'

with open(OUTPUT_PATH, 'w', encoding='utf-8') as artists_ids:
    json.dump(artists, artists_ids, indent=4, ensure_ascii=False)
    print('dumped!')

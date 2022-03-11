import json
import argparse
import glob

parser = argparse.ArgumentParser(description="get json file")
parser.add_argument('-i', '--input_directory')
args = parser.parse_args()

print("input:" + args.input_directory)

json_files = glob.glob(args.input_directory+ "/*.json")
for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as i:
        spotify_json = json.load(i)
    with open(json_file, 'w', encoding='utf-8') as o:
        json.dump(spotify_json, o, indent=4, ensure_ascii=False)
        print('dumped!')

print("the number of formated json : {}".format(len(json_files)))

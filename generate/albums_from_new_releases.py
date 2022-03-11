import os
import json
import glob


input_directory = os.path.join(os.getcwd(),'..','..','jsons', 'Browse', 'GetNewReleases', '2022-03-10')

ALBUMS_IDS_PATH = r'xxx\jsons\Albums\input\new_release_albums_ids.json'

albums = {}
with open(ALBUMS_IDS_PATH, 'r', encoding='utf-8') as albums_ids_file:
    albums = json.load(albums_ids_file)

new_releases_files = glob.glob(input_directory+ "/*.json")
for file in new_releases_files:
    with open(file, 'r', encoding='utf-8') as f:
        spotify_json = json.load(f)
    for album in spotify_json['albums']['items']:
        if 'JP' in album['available_markets']:
            albums[album['id']] = album['name']
        else:
            print('{} - {} is unavailable! id: {}'.format(album['artists'][0]['name'], album['name'], album['id']))

print("the number of the albums : {}".format(len(albums)))


with open(ALBUMS_IDS_PATH, 'w', encoding='utf-8') as albums_ids_file:
    json.dump(albums, albums_ids_file, indent=4, ensure_ascii=False)
    print('dumped!')

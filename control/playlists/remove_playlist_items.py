import json
import os
import logging
import traceback
import time
# load .env(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, OREGANIC_SPOTIFY_BASE_DIR) 
from dotenv import load_dotenv

from control.client import HeadlessAuth
load_dotenv()

from oreganic_spotify.generate import formatter

def load_config():
    config_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'input', 'config__get_playlist_items.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    logging.info('load config :', config)
    return config

def load_remove_tracks(playlist_id):
    remove_tracks_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'input', 'RemoveTracks', playlist_id + '.json')
    with open(remove_tracks_path, 'r', encoding='utf-8') as file:
        remove_tracks_json = json.load(file)
    logging.info('load remove tracks')
    return remove_tracks_json['remove_tracks']

def save_removed_items(playlist_id, removed_items):
    # load removed list of playlist
    before_removed_tracks_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'RemovePlaylistItems', playlist_id + '.json')
    if os.path.isfile(before_removed_tracks_path):
        with open(before_removed_tracks_path, 'r', encoding='utf-8') as file:
            before_removed_tracks = json.load(file)
        before_removed_tracks['removed_items'].extend(removed_items)
    else:
        before_removed_tracks = {'removed_items': removed_items}

    with open(before_removed_tracks_path, 'w', encoding='utf-8') as file:
        json.dump(before_removed_tracks, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    try:
        logging.basicConfig(filename='logs/remove_playlist_items.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        config = load_config()

        remove_tracks = load_remove_tracks(playlist_id=config['playlist_id'])

        removed_items = []
        sp = HeadlessAuth(scope="playlist-modify-private").create_spotipy_client()
        for remove_tracks_per_request in formatter.split_list(remove_tracks):
            response = sp.playlist_remove_all_occurrences_of_items(playlist_id=config['playlist_id'], items=remove_tracks_per_request)
            response['snapshot_id']
            
            removed_item = {
                'snapshot_id': response['snapshot_id'],
                'date': formatter.generate_formated_date(),
                'tracks': remove_tracks_per_request
                }
            removed_items.append(removed_item)
            '''
            {
                removed_items:[
                    snapshot_id:
                    date:
                    tracks:[

                    ]
                ]
            }
            '''

            time.sleep(0.5)

        save_removed_items(playlist_id=config['playlist_id'], removed_items=removed_items)
            
        logging.info('tracks removd (playlist_id:{})'.format(config['playlist_id']))


    except Exception as e:
        logging.error(traceback.format_exc())



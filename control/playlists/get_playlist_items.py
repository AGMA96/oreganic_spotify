import os
import json
import traceback

from oreganic_spotify.control.client import HeadlessAuth

def load_config():
    config_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'input', 'config__get_playlist_items.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    print('load config :', config)
    return config

def playlist_items(playlist_id, limit):
    sp = HeadlessAuth(scope="playlist-read-private").create_spotipy_client()
    playlist_tracks = sp.playlist_items(playlist_id=playlist_id, market='JP', limit=limit)
    return playlist_tracks

def write_playlist_items(playlist_id, playlist_items):
    playlist_items_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'GetPlaylistItems', playlist_id + '.json')
    with open(playlist_items_path, 'w', encoding='utf-8') as file:
        json.dump(playlist_items, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    try:
        config = load_config()
        playlist_tracks = playlist_items(playlist_id=config['playlist_id'], limit=config['limit'])
        write_playlist_items(config['playlist_id'], playlist_tracks)

    except Exception as e:
        print(traceback.format_exc())
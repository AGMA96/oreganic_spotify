import os
import json
import glob
import traceback

from oreganic_spotify.control.player import get_currently_playing_track
from oreganic_spotify.control.player import get_recently_played_tracks
from oreganic_spotify.control.playlists import get_playlist_items

# load .env(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, OREGANIC_SPOTIFY_BASE_DIR) 
from dotenv import load_dotenv
load_dotenv()

def load_config():
    config_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'input', 'config__get_playlist_items.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    print('load config :', config)
    return config

def load_first_track(playlist_id):
    playlist_items = get_playlist_items.playlist_items(playlist_id=playlist_id, limit=1)

    return playlist_items['items'][0]['track']['id']

def load_currently_playing(playlist_id):
    currently_playing = get_currently_playing_track.currently_playing()
    
    is_target_playlist = currently_playing['context']['uri'] == 'spotify:playlist:' + playlist_id
    track_id = currently_playing['item']['id']
    return is_target_playlist, track_id

def load_recently_played(playlist_id):
    recently_played = get_recently_played_tracks.current_user_recently_played()
    
    return [item['track']['id'] for item in recently_played['items'] if item['context']['uri'] == 'spotify:playlist:' + playlist_id]

def load_playlist_tracks(playlist_id, current_first_track_id):
    added_tracks_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'output', '*', playlist_id + '_*.json')
    playlist_tracks_paths = glob.glob(pathname=added_tracks_path, recursive=True)

    playlist_track_ids = []
    for playlist_tracks_path in playlist_tracks_paths:
        with open(playlist_tracks_path, 'r', encoding='utf-8') as playlist_tracks_file:
            playlist_tracks = json.load(playlist_tracks_file)
        
        for tracks_by_added in playlist_tracks['items']:
            track_ids_by_added = [tracks['id'] for tracks in tracks_by_added['tracks']]
            playlist_track_ids = playlist_track_ids + track_ids_by_added
    
    current_first_index = playlist_track_ids.index(current_first_track_id)
    current_playlist_track_ids = playlist_track_ids[current_first_index:]
    return current_playlist_track_ids

def get_recently_played_index(playlist_id):
    print("load playlist's first track...")
    first_track_id = load_first_track(playlist_id)

    print('load playlist tracks...')
    current_playlist_track_ids = load_playlist_tracks(playlist_id, first_track_id)

    print('load currently playing track...')
    search_track_id = ''
    is_target_playlist, current_playing_track_id = load_currently_playing(playlist_id)
    if is_target_playlist:
        search_track_id = current_playing_track_id
    else:
        print('load recently played tracks...')
        recently_played_track_ids = load_recently_played(playlist_id)
        search_track_id = recently_played_track_ids[0]

    print('get playlist index')
    recently_played_index = current_playlist_track_ids.index(search_track_id)

    return recently_played_index

if __name__ == '__main__':
    try:
        config = load_config()
        recently_played_index = get_recently_played_index(config['playlist_id'])

        print("playlist's offset is ", recently_played_index)
    except Exception as e:
        print(traceback.format_exc())


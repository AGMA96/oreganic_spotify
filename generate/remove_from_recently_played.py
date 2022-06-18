import os
import json
import glob
import traceback
import logging

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
    logging.info('load config :', config)
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

def save_remove_tracks(playlist_id):
    logging.debug("load playlist's first track...")
    first_track_id = load_first_track(playlist_id)

    logging.debug('load playlist tracks...')
    current_playlist_track_ids = load_playlist_tracks(playlist_id, first_track_id)

    logging.debug('load currently playing track...')
    search_track_id = ''
    is_target_playlist, current_playing_track_id = load_currently_playing(playlist_id)
    if is_target_playlist:
        search_track_id = current_playing_track_id
    else:
        logging.debug('load recently played tracks...')
        recently_played_track_ids = load_recently_played(playlist_id)
        search_track_id = recently_played_track_ids[0]

    logging.debug('get playlist index')
    search_track_index = current_playlist_track_ids.index(search_track_id)
    remove_tracks = current_playlist_track_ids[:search_track_index]

    remove_tracks_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Playlists', 'input', 'RemoveTracks', playlist_id + '.json')
    with open(remove_tracks_path, 'w', encoding='utf-8') as file:
        json.dump({'remove_tracks': remove_tracks}, file, indent=4, ensure_ascii=False)
    logging.debug('remove tracks dumped')

if __name__ == '__main__':
    try:
        config = load_config()
        remove_tracks = save_remove_tracks(config['playlist_id'])

        logging.info("remove tracks saved (playlist_id:", config['playlist_id'], ")")

        '''
        get currently_playing
        currently is in the playlist
        get first track of the playlist
        create list tracks_ids



        '''
    except Exception as e:
        logging.error(traceback.format_exc())


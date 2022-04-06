import os
import json
import traceback
import logging

from oreganic_spotify.generate.resume_from_recently_played import get_recently_played_index

# load .env(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, OREGANIC_SPOTIFY_BASE_DIR) 
from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def load_config():
    config_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Player', 'input', 'config__start_resume_playback.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    logging.info('load config :', config)
    return config

if __name__ == '__main__':
    try:
        logging.basicConfig(filename='logs/start_resume_playback.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        config = load_config()

        position = config['offset']
        if config['enable_offset_update']:
            playlist_id = config['context_uri'].split(':')[2]
            position = get_recently_played_index(playlist_id)

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))
        response = sp.start_playback(
            device_id=config['device_id'],
            context_uri=config['context_uri'],
            offset={"position": position}
        )

        logging.debug(response)
    except Exception as e:
        logging.error(traceback.format_exc())
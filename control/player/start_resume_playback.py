import os
import json

# load .env(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI) 
from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def load_config():
    config_path = os.path.join(os.getcwd(), 'jsons', 'Player', 'input', 'config__start_resume_playback.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    print('load config :', config)
    return config

if __name__ == '__main__':
    try:
        config = load_config()

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))
        sp.start_playback(
            device_id=config['device_id'],
            context_uri=config['context_uri'],
            offset={"position": config['offset']}
            )
    except Exception as e:
        print(e)
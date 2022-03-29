import os
import json

# load .env(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, OREGANIC_SPOTIFY_BASE_DIR) 
from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def current_user_recently_played():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-recently-played"))
    return sp.current_user_recently_played()

def write_recently_played(recently_played):
    recently_played_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Player', 'GetRecentlyPlayedTracks', 'recentlyPlayedTracks.json')
    with open(recently_played_path, 'w', encoding='utf-8') as file:
        json.dump(recently_played, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    try:
        recently_played = current_user_recently_played()
        write_recently_played(recently_played)

    except Exception as e:
        print(e)
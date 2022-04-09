import os
import json

from oreganic_spotify.control.client import HeadlessAuth

def current_user_recently_played():
    sp = HeadlessAuth(scope="user-read-recently-played").create_spotipy_client()
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
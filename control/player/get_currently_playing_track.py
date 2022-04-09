import os
import json

from oreganic_spotify.control.client import HeadlessAuth

def currently_playing():
    sp = HeadlessAuth(scope="user-read-currently-playing").create_spotipy_client()
    current_playing =sp.currently_playing(market='JP')
    return current_playing

def write_currently_playing(current_playing):
    current_playing_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Player', 'GetCurrentlyPlayingTrack', 'currentlyPlayingTrack.json')
    with open(current_playing_path, 'w', encoding='utf-8') as file:
        json.dump(current_playing, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    try:
        playing_track = currently_playing()
        write_currently_playing(playing_track)

    except Exception as e:
        print(e)
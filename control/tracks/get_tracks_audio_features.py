import spotipy
from spotipy.oauth2 import SpotifyOAuth

import time
import json
import glob
import os

def split_list(list):
    length = 100
    for idx in range(0, len(list), length):
        yield list[idx:idx + length]

def filter_acquired_ids(tracks_ids):
    ''' 取得済みのIDを差し引く '''
    TRACKS_AUDIO_FEATURES_PATHS = glob.glob(os.path.join(os.getcwd(), 'jsons', 'Tracks', 'GetTracksAudioFeatures', '*.json'))
    acquired_tracks_audio_features = {os.path.splitext(os.path.basename(path))[0] for path in TRACKS_AUDIO_FEATURES_PATHS}
    print("acquired track's audio features : ", str(len(acquired_tracks_audio_features)))

    filtered_ids = [id for id in tracks_ids if id not in acquired_tracks_audio_features]
    return filtered_ids


def load_track_ids(tracks_ids_path):
    ''' TRACK IDの一覧をファイルから読み込む '''
    with open(tracks_ids_path, 'r', encoding='utf-8') as liked_tracks_file:
        tracks_ids = json.load(liked_tracks_file)

    print('tracks ids : ', str(len(tracks_ids)))

    return tracks_ids


def main():
    print('start Get tracks audio features')

    liked_tracks_path = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'input', 'liked_tracks_ids.json')
    tracks_ids = load_track_ids(tracks_ids_path=liked_tracks_path)

    target_ids = filter_acquired_ids(tracks_ids=tracks_ids)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    for id_list in split_list(target_ids):
        tracks = sp.audio_features(tracks=id_list)

        for tracks_audio_features in tracks:
            tracks_audio_features_path = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'GetTracksAudioFeatures', '{}.json'.format(tracks_audio_features['id']))
            with open(tracks_audio_features_path, 'w', encoding="utf-8") as file:
                json.dump(tracks_audio_features, file, indent=4, ensure_ascii=False)
                print('dumps : ', file)

        time.sleep(1)


    print('done!')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
import time
import json
import glob
import os

from control.client import HeadlessAuth

def filter_acquired_ids(tracks_ids):
    ''' 取得済みのIDを差し引く '''
    TRACKS_AUDIO_FEATURES_PATHS = glob.glob(os.path.join(os.getcwd(), 'jsons', 'Tracks', 'GetTracksAudioAnalysis', '*.json'))
    acquired_tracks_analysis = {os.path.splitext(os.path.basename(path))[0] for path in TRACKS_AUDIO_FEATURES_PATHS}
    print("acquired track's analysis : ", str(len(acquired_tracks_analysis)))

    filtered_ids = [id for id in tracks_ids if id not in acquired_tracks_analysis]
    return filtered_ids


def load_track_ids(tracks_ids_path):
    ''' TRACK IDの一覧をファイルから読み込む '''
    with open(tracks_ids_path, 'r', encoding='utf-8') as tracks_file:
        tracks_ids = json.load(tracks_file)

    print('tracks ids : ', str(len(tracks_ids)))

    return tracks_ids


def main():
    print('start Get tracks audio features')

    liked_tracks_path = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'input', 'liked_tracks_ids.json')
    tracks_ids = load_track_ids(tracks_ids_path=liked_tracks_path)

    target_ids = filter_acquired_ids(tracks_ids=tracks_ids)

    sp = HeadlessAuth(scope="user-read-currently-playing").create_spotipy_client()
    for id in target_ids:
        analysis = sp.audio_analysis(track_id=id)

        tracks_analysis_path = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'GetTracksAudioAnalysis', '{}.json'.format(id))
        with open(tracks_analysis_path, 'w', encoding="utf-8") as file:
            json.dump(analysis, file, indent=4, ensure_ascii=False)
            print('dumps : ', file)

        time.sleep(2)


    print('done!')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
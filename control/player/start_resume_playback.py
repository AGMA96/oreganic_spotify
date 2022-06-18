from logging import handlers
import os
import json
import traceback
import logging

from oreganic_spotify.control.client import HeadlessAuth
from oreganic_spotify.generate.resume_from_recently_played import get_recently_played_index

def load_config():
    config_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Player', 'input', 'config__start_resume_playback.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    logging.info('load config :{}'.format(config))
    return config

if __name__ == '__main__':
    try:
        handlers = [logging.FileHandler('logs/start_resume_playback.log'), logging.StreamHandler()]
        logging.basicConfig(handlers=handlers, level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        config = load_config()

        position = config['offset']
        if config['enable_offset_update']:
            playlist_id = config['context_uri'].split(':')[2]
            position = get_recently_played_index(playlist_id)

#        sp = HeadlessAuth(scope="user-modify-playback-state").create_spotipy_client()
        sp = HeadlessAuth(scope="user-modify-playback-state,user-read-currently-playing,user-read-recently-played,playlist-read-private").create_spotipy_client()
        response = sp.start_playback(
            device_id=config['device_id'],
            context_uri=config['context_uri'],
            offset={"position": position}
        )

        if response is None:
            logging.info('Playback started')
            logging.debug(response)
        else:
            logging.error(response)

    except Exception as e:
        logging.error(traceback.format_exc())
from logging import handlers
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

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

LOGIN_USERNAME = os.environ.get("LOGIN_ID")
LOGIN_PASSWORD = os.environ.get("LOGIN_PW")

def load_config():
    config_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'jsons', 'Player', 'input', 'config__start_resume_playback.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    logging.info('load config :', config)
    return config

def create_spotipy_client(scope):
    spOAuth = SpotifyOAuth(scope=scope)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-logging')
    options.add_argument('--log-level=0')
    chrome_log_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'logs', 'chromedriver.log')

    with webdriver.Chrome(service=Service(log_path=chrome_log_path), options=options) as driver:
        driver.get(spOAuth.get_authorize_url())

        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.ID, 'login-username')))

        driver.find_element(By.ID, 'login-username').send_keys(LOGIN_USERNAME)
        driver.find_element(By.ID, 'login-password').send_keys(LOGIN_PASSWORD)
        driver.find_element(By.ID, 'login-button').click()

        wait.until_not(EC.presence_of_element_located((By.ID, 'login-username')))

        authorization_code = spOAuth.get_authorization_code(driver.current_url)

    access_token = spOAuth.get_access_token(as_dict=False, code=authorization_code)

    return spotipy.Spotify(auth=access_token)

if __name__ == '__main__':
    try:
        handlers = [logging.FileHandler('logs/start_resume_playback.log'), logging.StreamHandler()]
        logging.basicConfig(handlers=handlers, level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        config = load_config()

        position = config['offset']
        if config['enable_offset_update']:
            playlist_id = config['context_uri'].split(':')[2]
            position = get_recently_played_index(playlist_id)

        sp = create_spotipy_client(scope="user-modify-playback-state")
        response = sp.start_playback(
            device_id=config['device_id'],
            context_uri=config['context_uri'],
            offset={"position": position}
        )

        logging.debug(response)
    except Exception as e:
        logging.error(traceback.format_exc())
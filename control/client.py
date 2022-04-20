from linecache import checkcache
import os
from traceback import format_exc
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# load .env(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, OREGANIC_SPOTIFY_BASE_DIR, LOGIN_ID, LOGIN_PW) 
from dotenv import load_dotenv
load_dotenv()

import random, string

class HeadlessAuth():
    
    def __init__(self, scope=None) -> None:
        self.spOAuth = SpotifyOAuth(scope=scope, state=HeadlessAuth._generate_randomstr(10))
        self.authorization_code = None

    @staticmethod
    def _generate_randomstr(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _fetch_authorization_code(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        chrome_user_data_dir = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'chrome_data')
        options.add_argument('--user-data-dir={}'.format(chrome_user_data_dir))
        options.add_argument('--disable-gpu')
        options.add_argument('--enable-logging')
        options.add_argument('--log-level=0')
        chrome_log_path = os.path.join(os.environ.get("OREGANIC_SPOTIFY_BASE_DIR"), 'logs', 'chromedriver.log')

        with webdriver.Chrome(service=Service(log_path=chrome_log_path), options=options) as driver:
            authorize_url = self.spOAuth.get_authorize_url()
            try:
                driver.get(authorize_url)
            except Exception as e:
                logging.error(format_exc())


            wait = WebDriverWait(driver, 5)
            wait.until(EC.url_changes(authorize_url))
           
            if driver.find_elements_by_id('login-username') != []:

                LOGIN_USERNAME = os.environ.get("LOGIN_ID")
                LOGIN_PASSWORD = os.environ.get("LOGIN_PW")
                driver.find_element(By.ID, 'login-username').send_keys(LOGIN_USERNAME)
                driver.find_element(By.ID, 'login-password').send_keys(LOGIN_PASSWORD)
                driver.find_element(By.ID, 'login-button').click()

                wait.until_not(EC.presence_of_element_located((By.ID, 'login-username')))

            authorization_code = self.spOAuth.get_authorization_code(driver.current_url)
            if authorization_code == driver.current_url:
                raise Exception('failed to get authorization code')

            return authorization_code
    
    def checkCache(self):
        token_info = self.spOAuth.validate_token(self.spOAuth.cache_handler.get_cached_token())
        if token_info is not None:
            if self.spOAuth.is_token_expired(token_info):
                token_info = self.spOAuth.refresh_access_token(
                    token_info["refresh_token"]
                )
            return token_info["access_token"]

    def create_spotipy_client(self):
        access_token = self.checkCache()
        if access_token is None:
            if self.authorization_code is None:
                self.authorization_code = self._fetch_authorization_code()
                
            access_token = self.spOAuth.get_access_token(as_dict=False, code=self.authorization_code)

        return spotipy.Spotify(auth=access_token)
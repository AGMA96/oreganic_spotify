import time
import json
import datetime
import os

from control.client import HeadlessAuth

def generate_formated_date():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y-%m-%d')
    return d

sp = HeadlessAuth(scope="user-library-read").create_spotipy_client()

limit = 50
MAX_OFFSET = 20000
offset_limit = MAX_OFFSET
offset = 0

today = generate_formated_date()
os.makedirs(today, exist_ok=True)

print('start Get Users Saved Tracks')

while offset < MAX_OFFSET and offset < offset_limit:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset, market='JP')

    print('get result')

    users_saved_tracks_path = os.path.join(os.getcwd(), 'jsons', 'Tracks', 'GetUsersSavedTracks', '{}/offset_{:04d}.json'.format(today, offset))
    with open(users_saved_tracks_path, 'w', encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        print('dumps : ', f)

    offset_limit = int(results['total'])
    offset = offset + limit

    time.sleep(1)

print('done!')

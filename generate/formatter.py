import datetime
import logging

def generate_formated_date():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y-%m-%d')
    return d

def split_list(list):
    logging.debug('request objects length is ', len(list))
    length = 100 # Web API default maximum objects that can be sent at once
    for idx in range(0, len(list), length):
        yield list[idx:idx + length]

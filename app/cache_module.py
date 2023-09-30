import os
import json
import time

from app.settings import CONFIG

CACHE_EXPIRATION = CONFIG['CACHE_EXPIRATION']

def read_cache(cache_name: str):
    cache_file = 'app/cache/'+cache_name+'.json'
    if os.path.isfile(cache_file):
        cache = None
        with open(cache_file, 'r', encoding="utf-8") as f:
            try:
                cache = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return None
        if 'data' in cache and 'time' in cache:
            if int(time.time()) - int(cache['time']) < CACHE_EXPIRATION:
                return cache['data']
    return None

def write_cache(cache_name: str, data):
    os.makedirs('app/cache', exist_ok=True)
    cache_file = 'app/cache/'+cache_name+'.json'
    with open(cache_file, 'w+', encoding="utf-8") as f:
        f.write(json.dumps({
            'time': int(time.time()),
            'data': data
        }))

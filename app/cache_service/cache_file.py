import os
import json
import time

from app.cache_service.cache_interface import CacheInterface


CACHE_DIRECTORY = "cache"

class CacheFile(CacheInterface):

    def __init__(self, cache_name: str):
        super().__init__(cache_name)

    def read_cache(self):
        cache_file = CACHE_DIRECTORY + '/' + self.cache_name + '.json'
        if os.path.isfile(cache_file):
            cache = None
            with open(cache_file, 'r', encoding="utf-8") as f:
                try:
                    cache = json.loads(f.read())
                except json.decoder.JSONDecodeError:
                    return None
            if 'data' in cache and 'time' in cache:
                if int(time.time()) - int(cache['time']) < self.CACHE_EXPIRATION:
                    return cache['data']
        return None

    def write_cache(self, data):
        os.makedirs(CACHE_DIRECTORY, exist_ok=True)
        cache_file = CACHE_DIRECTORY + '/' + self.cache_name + '.json'
        with open(cache_file, 'w+', encoding="utf-8") as f:
            f.write(json.dumps({
                'time': int(time.time()),
                'data': data
            }))

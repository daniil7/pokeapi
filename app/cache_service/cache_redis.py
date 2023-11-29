import time
import pickle

import redis

from app.cache_service.cache_interface import CacheInterface
from app.settings import CONFIG

CACHE_ROOT = "cache"


class CacheRedis(CacheInterface):

    def __init__(self, cache_name: str):
        super().__init__(cache_name)
        self.redis_connection = redis.Redis(host=CONFIG['CACHE_REDIS_HOST'],
                                            port=CONFIG['CACHE_REDIS_PORT'],
                                            decode_responses=False)

    def __del__(self):
        self.redis_connection.close()

    def read_cache(self):
        cache_instance = CACHE_ROOT + ":" + self.cache_name
        p_cache = self.redis_connection.get(cache_instance)
        if p_cache is None:
            return None
        cache = pickle.loads(p_cache)
        if 'data' in cache and 'time' in cache:
            if int(time.time()) - int(cache['time']) < self.CACHE_EXPIRATION:
                return cache['data']
        return None

    def write_cache(self, data):
        cache_instance = CACHE_ROOT + ":" + self.cache_name
        cache = {
            'time': int(time.time()),
            'data': data,
        }
        self.redis_connection.set(cache_instance, pickle.dumps(cache))

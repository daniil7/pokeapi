from abc import ABC, abstractmethod

from app.settings import CONFIG


class CacheInterface(ABC):

    def __init__(self, cache_name: str):
        self.CACHE_EXPIRATION = CONFIG['CACHE_EXPIRATION']
        self.cache_name = cache_name

    @abstractmethod
    def read_cache(self):
        pass

    @abstractmethod
    def write_cache(self, data):
        pass

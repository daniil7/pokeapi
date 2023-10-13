from app.cache_service.cache_interface import CacheInterface


class CacheTest(CacheInterface):

    def __init__(self, cache_name: str):
        super().__init__(cache_name)

    def read_cache(self):
        return None

    def write_cahe(self, data):
        pass

from tests import UnitTestResponse
from app.cache_service.cache_file import CacheFile

class Test:

    def do():
        service = CacheFile('test')
        some_list = ['A', 'B', 'C', 'D']
        service.write_cache(some_list)
        if service.read_cache() == some_list:
            return UnitTestResponse.SUCCESS, "success"
        else:
            return UnitTestResponse.ERROR, "wrote and read data is not match"

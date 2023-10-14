from abc import ABC, abstractmethod

from app.settings import CONFIG


class FTPInterface(ABC):

    def __init__(self):
        self.host = CONFIG['FTP_HOST']
        self.port = CONFIG['FTP_PORT']
        self.user = CONFIG['FTP_USER']
        self.password = CONFIG['FTP_PASSWORD']

    @abstractmethod
    def scandir(self, path: str = '/') -> list:
        pass

    @abstractmethod
    def makedir(self, path: str):
        pass

    @abstractmethod
    def rmdir(self, path: str):
        pass

    @abstractmethod
    def read_file(self, path: str) -> str:
        pass

    @abstractmethod
    def write_file(self, path: str, data: str):
        pass

    @abstractmethod
    def del_file(self, path: str, data: str):
        pass

    @abstractmethod
    def rename(self, from_name: str, to_name: str):
        pass

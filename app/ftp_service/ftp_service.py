from app.ftp_service.ftp_interface import FTPInterface


class FTPService(FTPInterface):

    def __init__(self):
        super().__init__()

    def scandir(self, path = '/': str) -> list:
        return []

    def makedir(self, path: str):
        pass

    def rmdir(self, path: str):
        pass

    def read_file(self, path: str) -> str:
        return ""

    def write_file(self, path: str, data: str):
        pass

    def del_file(self, path: str, data: str):
        pass

    def rename(self, from_name: str, to_name: str):
        pass

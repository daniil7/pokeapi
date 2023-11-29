import ftplib
import io

from app.ftp_service.ftp_interface import FTPInterface, FTPErrorPermException


class FTPService(FTPInterface):

    def __handle_binary(self, more_data):
        self.binary_data.append(more_data)

    def __init__(self):
        super().__init__()
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.user, self.password)
        self.binary_data = []

    def __del__(self):
        self.ftp.close()

    def scandir(self, path: str = './') -> list:
        try:
            return self.ftp.nlst(path)
        except ftplib.error_perm as e:
            raise FTPErrorPermException(str(e))

    def makedir(self, path: str):
        try:
            return self.ftp.mkd(path)
        except ftplib.error_perm as e:
            raise FTPErrorPermException(str(e))

    def rmdir(self, path: str):
        try:
            return self.ftp.rmd(path)
        except ftplib.error_perm as e:
            raise FTPErrorPermException(str(e))

    def read_file(self, path: str) -> str:
        try:
            self.binary_data = []
            resp = self.ftp.retrbinary("RETR " + path,
                                       callback=self.__handle_binary)
            data = b"".join(self.binary_data)
            return data.decode("utf-8")
        except ftplib.error_perm as e:
            raise FTPErrorPermException(str(e))

    def write_file(self, path: str, data: str):
        try:
            file = io.BytesIO()
            file_wrapper = io.TextIOWrapper(file,
                                            encoding='utf-8',
                                            line_buffering=True)
            file_wrapper.write(data)
            file_wrapper.seek(0, 0)
            file.seek(0, 0)
            self.ftp.storbinary("STOR " + path, file)
        except ftplib.error_perm as e:
            raise FTPErrorPermException(str(e))

    def del_file(self, path: str):
        try:
            return self.ftp.delete(path)
        except ftplib.error_perm as e:
            raise FTPErrorPermException(str(e))

    def rename(self, from_name: str, to_name: str):
        try:
            return self.ftp.rename(from_name, to_name)
        except ftplib.error_perm as e:
            raise FTPErrorPermException(str(e))

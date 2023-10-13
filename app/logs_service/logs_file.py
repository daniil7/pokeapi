import os
import pathlib
import datetime

from app.logs_service.logs_interface import LogsInterface


LOGS_DIR = "logs"

class LogsFile(LogsInterface):

    def __init__(self, log_instance: str):
        self.log_instance = str(pathlib.Path(LOGS_DIR) / log_instance)
        os.makedirs(
                os.path.dirname(self.log_instance),
                exist_ok=True
            )

    def __write(self, file, data: str):
        current_datetime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        file.write(current_datetime + '\n' + data + '\n\n')

    def write(self, data: str):
        with open(self.log_instance, 'w+', encoding="utf-8") as file:
            self.__write(file, data)

    def write_add(self, data: str):
        with open(self.log_instance, 'a+', encoding="utf-8") as file:
            self.__write(file, data)

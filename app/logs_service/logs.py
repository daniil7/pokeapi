import os

LOGS_DIR = "logs"

class Logs:

    def __init__(self, log_path):
        self.log_path = LOGS_DIR + "/" + log_path
        os.makedirs(
                os.path.dirname(self.log_path),
                exist_ok=True
            )

    def __write(self, file, data: str, paragraph: bool = True):
        margin = "\n" if paragraph else ""
        file.write( margin + data + '\n' + margin)

    def write(self, data: str, paragraph: bool = True):
        with open(self.log_path, 'w+', encoding="utf-8") as file:
            self.__write(file, data, paragraph)

    def write_add(self, data: str, paragraph: bool = True):
        with open(self.log_path, 'a+', encoding="utf-8") as file:
            self.__write(file, data, paragraph)

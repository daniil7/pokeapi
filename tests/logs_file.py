from pathlib import Path

from tests import UnitTestResponse
from app.logs_service.logs_file import LogsFile, LOGS_DIR

class Test:

    @staticmethod
    def do():
        service = LogsFile('test/test_write')
        service.write("test line")
        with open(LOGS_DIR + '/test/test_write', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines = list(filter(lambda line: line != "\n", lines))
        lines = list(map(lambda line: line.replace("\n", ""), lines))
        if lines[1] != 'test line':
            return UnitTestResponse.ERROR, "log write: incorrect data"

        Path.unlink(Path(LOGS_DIR) / "test/test_write_add")

        service = LogsFile('test/test_write_add')
        service.write_add("test line 1")
        service.write_add("test line 2")
        with open(LOGS_DIR + '/test/test_write_add', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines = list(filter(lambda line: line != "\n", lines))
        lines = list(map(lambda line: line.replace("\n", ""), lines))
        if lines[1] != "test line 1" or lines[3] != "test line 2":
            return UnitTestResponse.ERROR, "log write_add: incorrect data"

        return UnitTestResponse.SUCCESS, "success"

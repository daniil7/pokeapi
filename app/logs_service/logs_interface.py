from abc import ABC, abstractmethod


class LogsInterface(ABC):

    @abstractmethod
    def __init__(self, log_instance: str):
        pass

    @abstractmethod
    def write(self, data: str):
        pass

    @abstractmethod
    def write_add(self, data: str):
        pass

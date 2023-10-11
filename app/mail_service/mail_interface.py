from abc import ABC, abstractmethod

from app.settings import CONFIG


class MailInterface(ABC):

    def __init__(self, mailto):
        self.mailto = mailto
        self.mailfrom = CONFIG['MAIL_FROM_ADDRESS']

    @abstractmethod
    def send_a_letter(self, message):
        pass

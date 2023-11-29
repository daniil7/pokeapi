import time

from app import services_provider
from app.mail_service.mail_interface import MailInterface
from app.helpers import randomword

LOG_DIR = "email"


class MailLog(MailInterface):

    def send_a_letter(self, message):
        log = services_provider.ServicesProvider.logs_service(
            LOG_DIR + "/" + str(int(time.time())) + "_" + randomword(10) +
            ".txt")
        log.write(data="FROM: " + self.mailfrom + "\n" + "TO: " + self.mailto +
                  "\n" + message)

import os
import time

from app.mail_service.mail_interface import MailInterface
from app.logs_service.logs import Logs

LOG_DIR = "email"

class MailLog(MailInterface):

    def __init__(self, mailto):
        super().__init__(mailto)

    def send_a_letter(self, message):
        log = Logs(LOG_DIR + "/" + str(int(time.time())) + ".txt")
        log.write(
                data = "FROM: " + self.mailfrom + "\n" +
                       "TO: " + self.mailto + "\n" +
                       message,
                paragraph = False
            )

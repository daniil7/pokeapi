import smtplib

from app.mail_service.mail_interface import MailInterface
from app.settings import CONFIG


class MailSMTP(MailInterface):

    def __init__(self, mailto):
        super().__init__(mailto)
        self.mailhost = CONFIG['MAIL_HOST']
        self.mailport = CONFIG['MAIL_PORT']
        self.mailpassword = CONFIG['MAIL_PASSWORD']

    def send_a_letter(self, message):
        smtpObj = smtplib.SMTP(self.mailhost, self.mailport)
        smtpObj.starttls()
        smtpObj.login(self.mailfrom, self.mailpassword)
        smtpObj.sendmail(
                self.mailfrom,
                self.mailto,
                message
            )
        smtpObj.quit()

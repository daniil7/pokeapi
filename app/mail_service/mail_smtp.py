import smtplib
from email.mime.text import MIMEText

from app.mail_service.mail_interface import MailInterface
from app.settings import CONFIG


class MailSMTP(MailInterface):

    def __init__(self, mailto):
        super().__init__(mailto)
        self.mailhost = CONFIG['MAIL_HOST']
        self.mailport = CONFIG['MAIL_PORT']
        self.mailpassword = CONFIG['MAIL_PASSWORD']

    def send_a_letter(self, message):

        msg = MIMEText(message.encode('utf-8'), _charset='utf-8')
        msg['Subject'] = 'PokeAPI'
        msg['From'] = self.mailfrom
        msg['To'] = self.mailto

        smtpObj = smtplib.SMTP(self.mailhost, self.mailport)
        smtpObj.starttls()
        smtpObj.login(self.mailfrom, self.mailpassword)
        smtpObj.sendmail(self.mailfrom, self.mailto, msg.as_string())
        smtpObj.quit()

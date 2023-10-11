from app.settings import CONFIG
from app.mail_service import mail_interface, mail_log, mail_smtp


class ServicesProvider:

    def mail_service(mailto: str) -> mail_interface.MailInterface:
        match CONFIG['MAIL_DRIVER']:
            case 'log':
                return mail_log.MailLog(mailto)
            case 'smtp':
                return mail_smtp.MailSMTP(mailto)

from app.settings import CONFIG
from app.mail_service import mail_interface, mail_log, mail_smtp


# Класс, предоставляющий различные сервисы.
class ServicesProvider:

    def mail_service(mailto: str) -> mail_interface.MailInterface:
        # Определение сервиса электронной почты в зависимости от настройки MAIL_DRIVER.
        match CONFIG['MAIL_DRIVER']:
            case 'log':
                # Если используется драйвер 'log', создается и возвращается объект MailLog.
                return mail_log.MailLog(mailto)
            case 'smtp':
                # Если используется драйвер 'smtp', создается и возвращается объект MailSMTP.
                return mail_smtp.MailSMTP(mailto)

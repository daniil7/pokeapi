from app.settings import CONFIG
from app.mail_service import mail_interface, mail_test, mail_log, mail_smtp
from app.logs_service import logs_interface, logs_test, logs_file
from app.cache_service import cache_interface, cache_test, cache_file
from app.ftp_service import ftp_interface, ftp_test, ftp_service


# Класс, предоставляющий различные сервисы.
class ServicesProvider:

    def mail_service(mailto: str) -> mail_interface.MailInterface:
        if CONFIG['TEST_MODE']:
            return mail_test.MailTest(mailto)
        # Определение сервиса электронной почты в зависимости от настройки MAIL_DRIVER.
        match CONFIG['MAIL_DRIVER']:
            case 'log':
                # Если используется драйвер 'log', создается и возвращается объект MailLog.
                return mail_log.MailLog(mailto)
            case 'smtp':
                # Если используется драйвер 'smtp', создается и возвращается объект MailSMTP.
                return mail_smtp.MailSMTP(mailto)

    def logs_service(log_instance: str) -> logs_interface.LogsInterface:
        if CONFIG['TEST_MODE']:
            return logs_test.LogsTest(log_instance)
        # Определение сервиса логирования
        match CONFIG['LOGS_DRIVER']:
            case 'file':
                return logs_file.LogsFile(log_instance)

    def cache_service(cache_instance: str) -> cache_interface.CacheInterface:
        if CONFIG['TEST_MODE']:
            return cache_test.CacheTest(cache_instance)
        # Определение сервиса кэширования
        match CONFIG['CACHE_DRIVER']:
            case 'file':
                return cache_file.CacheFile(cache_instance)

    def ftp_service() -> ftp_interface.FTPInterface:
        if CONFIG['TEST_MODE']:
            return ftp_test.FTPTest()
        # Определение сервиса FTP
        match CONFIG['FTP_DRIVER']:
            case 'ftp':
                return ftp_service.FTPService()
            case 'none':
                return ftp_test.FTPTest()

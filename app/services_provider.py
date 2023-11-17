from app.settings import CONFIG
from app.mail_service import mail_interface, mail_test, mail_log, mail_smtp
from app.logs_service import logs_interface, logs_test, logs_file
from app.cache_service import cache_interface, cache_test, cache_file, cache_redis
from app.ftp_service import ftp_interface, ftp_test, ftp_service

import functools


testing_plug = None

def inject_test(test_service):
    # Декоратор встраивания функционала тестирования
    # Если включён TEST_MODE, вместо сервисов подключаются пустышки
    # Если установлен testing_plug, он подставляется вместо сервиса
    def _inject_test(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if CONFIG['TEST_MODE']:
                return test_service(*args, **kwargs)
            if testing_plug is not None:
                return testing_plug
            return func(*args, **kwargs)
        return wrapper
    return _inject_test

# Класс, предоставляющий различные сервисы.
class ServicesProvider:

    @inject_test(mail_test.MailTest)
    def mail_service(mailto: str) -> mail_interface.MailInterface:
        # Определение сервиса электронной почты в зависимости от настройки MAIL_DRIVER.
        match CONFIG['MAIL_DRIVER']:
            case 'log':
                return mail_log.MailLog(mailto)
            case 'smtp':
                return mail_smtp.MailSMTP(mailto)
            case 'none':
                return mail_test.MailTest(mailto)

    @inject_test(logs_test.LogsTest)
    def logs_service(log_instance: str) -> logs_interface.LogsInterface:
        # Определение сервиса логирования
        match CONFIG['LOGS_DRIVER']:
            case 'file':
                return logs_file.LogsFile(log_instance)
            case 'none':
                return logs_test.LogsTest(log_instance)

    @inject_test(cache_test.CacheTest)
    def cache_service(cache_instance: str) -> cache_interface.CacheInterface:
        # Определение сервиса кэширования
        match CONFIG['CACHE_DRIVER']:
            case 'file':
                return cache_file.CacheFile(cache_instance)
            case 'redis':
                return cache_redis.CacheRedis(cache_instance)
            case 'none':
                return cache_test.CacheTest(cache_instance)

    @inject_test(ftp_test.FTPTest)
    def ftp_service() -> ftp_interface.FTPInterface:
        # Определение сервиса FTP
        match CONFIG['FTP_DRIVER']:
            case 'ftp':
                return ftp_service.FTPService()
            case 'none':
                return ftp_test.FTPTest()

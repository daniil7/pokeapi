import os
from dotenv import load_dotenv


load_dotenv()

CONFIG = {

    'APP_URL': os.environ.get('APP_URL', 'http://localhost:5000'),
    'APP_SECRET_KEY': os.environ.get('APP_SECRET_KEY', None),
    'SECURITY_PASSWORD_SALT': os.environ.get('SECURITY_PASSWORD_SALT', None),

    'TEST_MODE': os.environ.get('TEST_MODE', 'FALSE') == 'TRUE',

    'LOGS_DRIVER': os.environ.get('LOGS_DRIVER', 'file'),

    'CACHE_DRIVER': os.environ.get('CACHE_DRIVER', 'file'),
    'CACHE_EXPIRATION': int(os.environ.get('CACHE_EXPIRATION', '86400')),
    'CACHE_REDIS_HOST': os.environ.get('CACHE_REDIS_HOST', 'localhost'),
    'CACHE_REDIS_PORT': int(os.environ.get('CACHE_REDIS_PORT', '6379')),

    'DB_DRIVER': os.environ.get('DB_DRIVER', 'sqlite'),
    'DB_USER': os.environ.get('DB_USER', 'admin'),
    'DB_PASSWORD': os.environ.get('DB_PASSWORD', 'admin'),
    'DB_DATABASE': os.environ.get('DB_DATABASE', 'db'),
    'DB_HOST': os.environ.get('DB_HOST', 'localhost'),
    'DB_PORT': os.environ.get('DB_PORT', '3306'),

    'MAIL_DRIVER': os.environ.get('MAIL_DRIVER', 'log'),
    'MAIL_HOST': os.environ.get('MAIL_HOST', ''),
    'MAIL_PORT': os.environ.get('MAIL_PORT', ''),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD', ''),
    'MAIL_FROM_ADDRESS': os.environ.get('MAIL_FROM_ADDRESS', ''),
    'MAIL_TO_ADDRESS': os.environ.get('MAIL_TO_ADDRESS', ''),

    'FTP_DRIVER': os.environ.get('FTP_DRIVER', 'none'),
    'FTP_HOST': os.environ.get('FTP_HOST', '127.0.0.1'),
    'FTP_PORT': int(os.environ.get('FTP_PORT', '21')),
    'FTP_USER': os.environ.get('FTP_USER', 'admin'),
    'FTP_PASSWORD': os.environ.get('FTP_PASSWORD', 'admin'),
}

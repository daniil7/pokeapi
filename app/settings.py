import os
from dotenv import load_dotenv


load_dotenv()

CONFIG = {
    'CACHE_EXPIRATION': int(os.environ.get('CACHE_EXPIRATION', '86400')),

    'DB': os.environ.get('DB', 'sqlite'),
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
}

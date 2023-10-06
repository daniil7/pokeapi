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
}

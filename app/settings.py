import os
from dotenv import load_dotenv
load_dotenv()

CONFIG = {
    'CACHE_EXPIRATION': int(os.environ.get('CACHE_EXPIRATION')) \
        if os.environ.get('CACHE_EXPIRATION') is not None else 86400,
}

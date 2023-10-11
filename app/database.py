from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import CONFIG


# Создание переменной для хранения объекта SQLAlchemy Engine.
engine = None

# Выбор типа базы данных в зависимости от значения настройки DB.
match CONFIG['DB']:
    case 'postgresql':
        # Если DB указана как 'postgresql', создается соответствующий объект Engine.
        engine = create_engine(f"postgresql+psycopg2://{CONFIG['DB_USER']}:{CONFIG['DB_PASSWORD']}@{CONFIG['DB_HOST']}:{CONFIG['DB_PORT']}/{CONFIG['DB_DATABASE']}")
    case _:
        # Если DB не указана как 'postgresql', создается объект Engine для SQLite.
        SQLITE_DIRECTORY = 'database'
        Path(SQLITE_DIRECTORY).mkdir(parents=True, exist_ok=True)
        Path(SQLITE_DIRECTORY+'/sqlite3.db').touch()
        engine = create_engine('sqlite:///database/sqlite3.db')

# Создание сессии базы данных с использованием SQLAlchemy.
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Создание базового класса для объявления моделей данных SQLAlchemy.
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Импорт моделей данных при инициализации базы данных.
    import app.models
    # Создание таблиц базы данных на основе объявленных моделей.
    Base.metadata.create_all(bind=engine)

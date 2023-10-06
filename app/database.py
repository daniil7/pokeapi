from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import CONFIG


engine = None

match CONFIG['DB']:
    case 'postgresql':
        engine = create_engine(f"postgresql+psycopg2://{CONFIG['DB_USER']}:{CONFIG['DB_PASSWORD']}@{CONFIG['DB_HOST']}:{CONFIG['DB_PORT']}/{CONFIG['DB_DATABASE']}")
    case _:
        SQLITE_DIRECTORY = 'database'
        Path(SQLITE_DIRECTORY).mkdir(parents=True, exist_ok=True)
        Path(SQLITE_DIRECTORY+'/sqlite3.db').touch()
        engine = create_engine('sqlite:///database/sqlite3.db')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)

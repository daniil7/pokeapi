import datetime

from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import UserMixin

from app.database import Base


# Модель БД для хранения истории боёв покемонов
class BattlesHistory(Base):
    __tablename__ = 'battles_history'
    id = Column(Integer, primary_key=True)
    user_pokemon = Column(String(50), unique=False)
    enemy_pokemon = Column(String(50), unique=False)
    user_score = Column(Integer)
    enemy_score = Column(Integer)
    user_id = Column(Integer, nullable=True)

    created_at = Column(DateTime(), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.datetime.utcnow,  onupdate=datetime.datetime.utcnow)

    def __init__(
            self,
            user_pokemon,
            enemy_pokemon,
            user_score,
            enemy_score
        ):
        self.user_pokemon = user_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.user_score = user_score
        self.enemy_score = enemy_score

    def __repr__(self):
        return f'<Battle {self.id!r}>'

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(150), nullable=True)
    email = Column(String(100), nullable=True, unique=True)
    email_verified_at = Column(DateTime(), nullable=True, default=None)
    created_at = Column(DateTime(), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.datetime.utcnow,  onupdate=datetime.datetime.utcnow)

    provider_id = Column(String(64), nullable=True)

    def is_verified(self):
        return (self.email_verified_at is not None) or (self.provider_id is not None)

    def __repr__(self):
        return f"<{self.id}:{self.username}>"

    def set_password(self, password: str):
        self.password = generate_password_hash(password, method='pbkdf2', salt_length=16)

    def check_password(self,  password: str):
        return check_password_hash(self.password, password)

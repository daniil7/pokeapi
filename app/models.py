from sqlalchemy import Column, Integer, String

from app.database import Base


# Модель БД для хранения истории боёв покемонов
class BattlesHistory(Base):
    __tablename__ = 'battles_history'
    id = Column(Integer, primary_key=True)
    user_pokemon = Column(String(50), unique=False)
    enemy_pokemon = Column(String(50), unique=False)
    user_score = Column(Integer)
    enemy_score = Column(Integer)

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

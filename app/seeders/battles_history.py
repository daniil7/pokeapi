import random
from datetime import datetime, timedelta

from app.database import db_session
from app.models import BattlesHistory
from app.database import Base
from app.pokemon_api import request_pokemons

class Seeder:

    def __init__(self):
        self.pokemons = request_pokemons()

    def make(self) -> Base:
        winner = random.choice([True, False])
        time = datetime.today() - timedelta(days=random.randint(0, 14))
        model = BattlesHistory(
            user_pokemon = random.choice(self.pokemons)['name'],
            enemy_pokemon = random.choice(self.pokemons)['name'],
            user_score = 3 if winner else random.randint(0, 2),
            enemy_score = random.randint(0, 2) if winner else 3,
        )
        model.created_at = time
        model.updated_at = time
        return model

    def fill(self, num: int):
        for _ in range(num):
            model = self.make()
            db_session.add(model)
            db_session.commit()

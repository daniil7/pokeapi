import random

from flask import render_template

from app.pokemon_api import request_pokemons, request_pokemon

def battle(user_pokemon_name: str):
    # Сцена с боем между покемоном пользователя и случайно выбранным врагом.
    user_pokemon = request_pokemon(user_pokemon_name)
    enemy_pokemon_name = random.choice(request_pokemons())['name']
    enemy_pokemon = request_pokemon(enemy_pokemon_name)
    user_pokemon_stats = {}
    for stat in user_pokemon['stats']:
        user_pokemon_stats[stat['stat']['name']] = stat['base_stat']
    enemy_pokemon_stats = {}
    for stat in enemy_pokemon['stats']:
        enemy_pokemon_stats[stat['stat']['name']] = stat['base_stat']

    return render_template(
        "battle.html",
        title='Pokemon',
        user_pokemon=user_pokemon,
        user_pokemon_name=user_pokemon_name,
        enemy_pokemon=enemy_pokemon,
        enemy_pokemon_name=enemy_pokemon_name,
        user_pokemon_stats=user_pokemon_stats,
        enemy_pokemon_stats=enemy_pokemon_stats
    )

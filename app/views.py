import random
import json

from flask import render_template, make_response, request
from app import app
from app.pokemon_api import request_pokemons, request_pokemon, APIRequestException
from app.database import db_session
from app.models import BattlesHistory
from app.settings import CONFIG
from app.services_provider import ServicesProvider


def api_error_response(error_message):
    # Функция для создания JSON-ответа с ошибкой.
    return {'error', error_message}

@app.route('/')
@app.route('/index')
def index():
    # Главная страница приложения, отображает шаблон "index.html".
    return render_template("index.html", title='Home')

@app.route('/pokemon/<pokemon_name>')
def pokemon(pokemon_name):
    # Отображает информацию о конкретном покемоне по его имени.
    pokemon = request_pokemon(pokemon_name)
    return render_template(
        "pokemon.html",
        title='Pokemon',
        pokemon=pokemon,
        pokemon_name=pokemon_name
    )

@app.route('/battle/<user_pokemon_name>')
def battle(user_pokemon_name):
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

@app.route('/api/pokemon')
def api_pokemons():
    # API-маршрут для получения списка покемонов.
    try:
        pokemons = request_pokemons()
    except APIRequestException as e:
        return api_error_response(e.message)

    return app.response_class(
        response=json.dumps(pokemons),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/pokemon/<pokemon_name>')
def api_certain_pokemon(pokemon_name):
    # API-маршрут для получения информации о конкретном покемоне по его имени.
    try:
        return app.response_class(
            response=json.dumps(request_pokemon(pokemon_name)),
            status=200,
            mimetype='application/json'
        )
    except APIRequestException as e:
        return api_error_response(e.message)

@app.route('/api/pokemon-sprite/<pokemon_name>')
def api_pokemon_sprite(pokemon_name):
    # API-маршрут для получения спрайта покемона по его имени.
    try:
        return app.response_class(
            response=request_pokemon(pokemon_name)['sprites']['front_default'],
            status=200,
            mimetype='text/plain'
        )
    except APIRequestException as e:
        return api_error_response(e.message)

@app.route('/api/battle/write-result', methods=['POST'])
def api_battle_write_result():
    # API-маршрут для записи результатов битвы.
    score = request.json
    battle_result = BattlesHistory(
        score['user_pokemon']['name'],
        score['enemy_pokemon']['name'],
        score['user_pokemon']['score'],
        score['enemy_pokemon']['score'],
    )
    db_session.add(battle_result)
    db_session.commit()
    mail_service = ServicesProvider.mail_service(CONFIG['MAIL_TO_ADDRESS'])
    mail_service.send_a_letter(
        'user pokemon: ' +
        str(score['user_pokemon']['name']) + ' ' +
        str(score['user_pokemon']['score']) + '\n' +
        'enemy pokemon: ' +
        str(score['enemy_pokemon']['name']) + ' ' +
        str(score['enemy_pokemon']['score'])
    )
    return 'success'

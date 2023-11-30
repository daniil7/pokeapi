import datetime
import pathlib
import functools
import random
import json

import jsonschema
from flask import render_template, make_response, request, redirect
from flask_login import login_user, logout_user
from sqlalchemy import exists as db_exists, or_ as db_or

from app import services_provider
from app import app
from app.pokemon_api import request_pokemons, request_pokemon, APIRequestException
from app.database import db_session
from app.models import BattlesHistory, User
from app.settings import CONFIG
from app.ftp_service.ftp_interface import FTPErrorPermException


def content_type(value: str):
    # Декоратор проверки content-type
    def _content_type(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            required_types = list(map(lambda t: t.strip(),
                                      value.replace(" ", "").lower().split(";")))
            request_types  = list(map(lambda t: t.strip(),
                                      request.headers.get("Content-Type").replace(" ", "").lower().split(";")))
            if required_types != request_types:
                error_message = {
                    'error': 'not supported Content-Type'
                }
                return make_response(error_message, 400)

            return func(*args,**kwargs)
        return wrapper
    return _content_type

@app.route('/')
@app.route('/index')
def index_route():
    # Главная страница приложения, отображает шаблон "index.html".
    return render_template("index.html", title='Home')

@app.route('/pokemon/<pokemon_name>')
def pokemon_route(pokemon_name):
    # Отображает информацию о конкретном покемоне по его имени.
    pokemon = request_pokemon(pokemon_name)
    return render_template(
        "pokemon.html",
        title='Pokemon',
        pokemon=pokemon,
        pokemon_name=pokemon_name
    )

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form.get("password") != request.form.get("password_confirmation") or \
            db_session.query(db_exists().where(
                db_or(
                    User.username == request.form.get('username'),
                    User.email == request.form.get('email')
                )
            )).scalar():
            return redirect("/register")
        user = User(username=request.form.get("username"),
                    email=request.form.get("email"))
        user.set_password(request.form.get("password"))
        db_session.add(user)
        db_session.commit()
        return redirect('/login')
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        if user is not None and user.check_password(request.form.get("password")):
            login_user(user)
            return redirect('/')
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route('/battle/<user_pokemon_name>')
def battle_route(user_pokemon_name):
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

#
#
# API BLOCK
#

@app.route('/api/pokemon')
def api_pokemons_route():
    # API-маршрут для получения списка покемонов.
    try:
        pokemons = request_pokemons()
    except APIRequestException as e:
        return make_response({'error': str(e)}, 404)

    return app.response_class(
        response=json.dumps(pokemons),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/pokemon/<pokemon_name>')
def api_certain_pokemon_route(pokemon_name):
    # API-маршрут для получения информации о конкретном покемоне по его имени.
    try:
        return app.response_class(
            response=json.dumps(request_pokemon(pokemon_name)),
            status=200,
            mimetype='application/json'
        )
    except APIRequestException as e:
        return make_response({'error': str(e)}, 404)

@app.route('/api/battle/write-result', methods=['POST'])
@content_type('application/json; charset=UTF-8')
def api_battle_write_result_route():
    # API-маршрут для записи результатов битвы.

    score = request.json

    # Валидация json
    required_schema = {
        'type': 'object',
        'properties': {
            'user_pokemon': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'score': {'type': 'number'}
                },
                "required": ["name", "score"]
            },
            'enemy_pokemon': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'score': {'type': 'number'}
                },
                "required": ["name", "score"]
            }
        },
        "required": ["user_pokemon", "enemy_pokemon"]
    }
    try:
        jsonschema.validate(instance=request.json, schema=required_schema)
    except Exception:
        return make_response({'error': 'invalid json schema', 'test': score}, 400)

    battle_result = BattlesHistory(
        score['user_pokemon']['name'],
        score['enemy_pokemon']['name'],
        score['user_pokemon']['score'],
        score['enemy_pokemon']['score'],
    )
    db_session.add(battle_result)
    db_session.commit()
    mail_service = services_provider.ServicesProvider.mail_service(CONFIG['MAIL_TO_ADDRESS'])
    mail_service.send_a_letter(
        'user pokemon: ' +
        str(score['user_pokemon']['name']) + ' ' +
        str(score['user_pokemon']['score']) + '\n' +
        'enemy pokemon: ' +
        str(score['enemy_pokemon']['name']) + ' ' +
        str(score['enemy_pokemon']['score'])
    )

    return 'success'

@app.route('/api/ftp/save-pokemon', methods=['POST'])
@content_type('text/plain; charset=UTF-8')
def api_save_pokemon_to_ftp_route():
    # API-маршрут для записи информации о покемоне на внешнем ftp сервере

    pokemon_name = request.data.decode("utf-8")
    try:
        pokemon = request_pokemon(pokemon_name)
    except APIRequestException as e:
        return make_response({'error': str(e)}, 404)
    ftp_service = services_provider.ServicesProvider.ftp_service()
    dir_name = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        ftp_service.makedir(dir_name)
    except FTPErrorPermException as e:
        pass
    try:
        ftp_service.write_file(
                str(pathlib.Path(dir_name) / (pokemon_name + ".md")),
                f"# {pokemon_name} \n" +
                "\n".join(
                    [
                        "- " + stat['stat']['name'] + ": " + str(stat['base_stat'])
                        for stat in pokemon['stats']
                    ]
                )
            )
    except FTPErrorPermException as e:
        return make_response({'error': str(e)}, 500)

    return "success"

import functools

from flask import make_response, request, abort
from flask_login import current_user

from app import app

from app.controllers import auth as auth_controller
from app.controllers import show_pokemons as show_pokemons_controller
from app.controllers import battle as battle_controller
from app.controllers import oauth as oauth_controller
from app.controllers.api import retrive_pokemons as retrive_pokemons_api_controller
from app.controllers.api import battle as battle_api_controller
from app.controllers.api import data_dumping as data_dumping_api_controller


# Middlewares
#
#

# Декоратор проверки авторизации
def login_required():
    def _content_type(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            if not current_user.is_authenticated:
                abort(401)
            return func(*args,**kwargs)
        return wrapper
    return _content_type

# Декоратор проверки content-type
def content_type(value: str):
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


# Authentication
#
#

@app.route('/register', methods=["GET", "POST"])
def register():
    return auth_controller.register()

@app.route("/login", methods=["GET", "POST"])
def login():
    return auth_controller.login()

@app.route("/logout")
def logout():
    return auth_controller.logout()

@app.route('/confirm/<token>')
def confirm_email(token):
    return auth_controller.confirm_email(token)

@app.route('/second-factor/<token>')
def second_factor(token):
    return auth_controller.second_factor(token)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    return oauth_controller.oauth_authorize(provider)

@app.route('/callback/<provider>')
def oauth_callback(provider):
    return oauth_controller.oauth_callback(provider)

@app.route('/oauth-confirm-registration', methods=["GET", "POST"])
def oauth_confirm_registration():
    return oauth_controller.oauth_confirm_registration()

# Show information about pokemons
#
#

@app.route('/')
@app.route('/index')
def index():
    # Главная страница приложения, отображает шаблон "index.html".
    return show_pokemons_controller.index_pokemons()

@app.route('/pokemon/<pokemon_name>')
def show_pokemon(pokemon_name):
    # Отображает информацию о конкретном покемоне по его имени.
    return show_pokemons_controller.show_pokemon(pokemon_name)


# Battle of pokemons
#
#

@app.route('/battle/<user_pokemon_name>')
def battle(user_pokemon_name):
    # Сцена с боем между покемоном пользователя и случайно выбранным врагом.
    return battle_controller.battle(user_pokemon_name)


# API
#
#

# Retrive pokemons

@app.route('/api/pokemon')
def api_pokemons():
    # API-маршрут для получения списка покемонов.
    return retrive_pokemons_api_controller.api_pokemons()

@app.route('/api/pokemon/<pokemon_name>')
def api_certain_pokemon_route(pokemon_name):
    # API-маршрут для получения информации о конкретном покемоне по его имени.
    return retrive_pokemons_api_controller.api_certain_pokemon(pokemon_name)

# Battle

@app.route('/api/battle/write-result', methods=['POST'])
@content_type('application/json; charset=UTF-8')
def api_battle_write_result_route():
    # API-маршрут для записи результатов битвы.
    return battle_api_controller.api_battle_write_result_route()

# Save pokemons

@app.route('/api/ftp/save-pokemon', methods=['POST'])
@content_type('text/plain; charset=UTF-8')
def api_dump_pokemons():
    # API-маршрут для записи информации о покемоне на внешнем ftp сервере
    data_dumping_api_controller.api_dump_pokemons()

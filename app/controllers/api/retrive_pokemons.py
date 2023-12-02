import json

from flask import make_response

from app import app
from app.pokemon_api import request_pokemons, request_pokemon, APIRequestException


def api_pokemons():
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

def api_certain_pokemon(pokemon_name):
    # API-маршрут для получения информации о конкретном покемоне по его имени.
    try:
        return app.response_class(
            response=json.dumps(request_pokemon(pokemon_name)),
            status=200,
            mimetype='application/json'
        )
    except APIRequestException as e:
        return make_response({'error': str(e)}, 404)

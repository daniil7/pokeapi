from flask import render_template, make_response
from app import app

from app.pokemon_api import request_pokemons, request_pokemon, APIRequestException
import json

def api_error_response(error_message):
    return {'error', error_message}

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title = 'Home')

@app.route('/pokemon/<pokemon_name>')
def pokemon(pokemon_name):
    pokemon = request_pokemon(pokemon_name)
    return render_template(
        "pokemon.html",
        title = 'Pokemon',
        pokemon = pokemon,
        pokemon_name = pokemon_name)

@app.route('/api/pokemon')
def api_pokemons():
    try:
        return app.response_class(
            response=json.dumps(request_pokemons()),
            status=200,
            mimetype='application/json'
        )
    except APIRequestException as e:
        return api_error_response(e.message)

@app.route('/api/pokemon/<pokemon_name>')
def api_certain_pokemon(pokemon_name):
    try:
        return app.response_class(
            response=json.dumps(request_pokemon(pokemon_name)),
            status=200,
            mimetype='application/json'
        )
    except APIRequestException as e:
        return api_error_response(e.message)

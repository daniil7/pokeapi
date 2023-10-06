from flask import render_template, make_response
from app import app
import random

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

@app.route('/battle/<user_pokemon_name>')
def battle(user_pokemon_name):
    user_pokemon = request_pokemon(user_pokemon_name)
    enemy_pokemon_name = random.choice(request_pokemons())['name']
    enemy_pokemon = request_pokemon(enemy_pokemon_name)
    return render_template(
        "battle.html",
        title = 'Pokemon',
        user_pokemon = user_pokemon,
        user_pokemon_name = user_pokemon_name,
        enemy_pokemon = enemy_pokemon,
        enemy_pokemon_name = enemy_pokemon_name)

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

@app.route('/api/pokemon-sprite/<pokemon_name>')
def api_pokemon_sprite(pokemon_name):
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
    return '';

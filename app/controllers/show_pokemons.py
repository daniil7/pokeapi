from flask import render_template

from app.pokemon_api import request_pokemon

def index_pokemons():
    # Главная страница приложения, отображает шаблон "index.html".
    return render_template("index.html", title='Home')

def show_pokemon(pokemon_name):
    # Отображает информацию о конкретном покемоне по его имени.
    pokemon = request_pokemon(pokemon_name)
    return render_template(
        "pokemon.html",
        title='Pokemon',
        pokemon=pokemon,
        pokemon_name=pokemon_name
    )

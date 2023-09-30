import requests
from app.cache_module import read_cache, write_cache

API_ROUTE = "https://pokeapi.co/api/v2/"

class APIRequestException(Exception):
    pass

def request_count():
    r = requests.get(API_ROUTE+'pokemon?limit=1')
    if r.status_code != 200:
        raise APIRequestException('could not request count of pokemons, status code: '+r.status_code)
    return r.json()['count']

def request_pokemons():

    cache = read_cache('pokemons')
    if cache is not None:
        return cache

    count = request_count()
    r = requests.get(API_ROUTE+'pokemon?limit='+str(count))
    if r.status_code != 200:
        raise APIRequestException('could not request pokemons, status code: '+r.status_code)
    response_data = r.json()['results']

    write_cache('pokemons', response_data)

    return response_data

def request_pokemon(pokemon_name: str):

    cache = read_cache('pokemon-'+pokemon_name)
    if cache is not None:
        return cache

    r = requests.get(API_ROUTE+'pokemon/'+pokemon_name)
    if r.status_code != 200:
        raise APIRequestException('could not request pokemon '+pokemon_name+', status code: '+r.status_code)
    response_data = r.json()

    write_cache('pokemon-'+pokemon_name, response_data)

    return response_data

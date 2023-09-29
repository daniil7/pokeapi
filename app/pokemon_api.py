import requests

API_ROUTE = "https://pokeapi.co/api/v2/"

class APIRequestException(Exception):
    pass

def request_count():
    r = requests.get(API_ROUTE+'pokemon?limit=1')
    if r.status_code != 200:
        raise APIRequestException('could not request count of pokemons, status code: '+r.status_code)
    return r.json()['count']

def request_pokemons():
    count = request_count()
    r = requests.get(API_ROUTE+'pokemon?limit='+str(count))
    if r.status_code != 200:
        raise APIRequestException('could not request pokemons, status code: '+r.status_code)
    return r.json()['results']

def request_pokemon(pokemon_name: str):
    r = requests.get(API_ROUTE+'pokemon/'+pokemon_name)
    if r.status_code != 200:
        raise APIRequestException('could not request pokemon '+pokemon_name+', status code: '+r.status_code)
    return r.json()

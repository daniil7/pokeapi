import requests

import app.services_provider as services_provider


# Константа, представляющая базовый URL для запросов к API Pokemon.
API_ROUTE = "https://pokeapi.co/api/v2/"

# Исключение, которое будет возбуждено в случае проблем при выполнении запроса к API.
class APIRequestException(Exception):
    pass

# Функция для выполнения запроса и получения количества покемонов в API.
def request_count():
    r = requests.get(API_ROUTE + 'pokemon?limit=1')
    if r.status_code != 200:
        raise APIRequestException('Could not request count of pokemons, status code: ' + str(r.status_code))
    return r.json()['count']

# Функция для выполнения запроса и получения списка покемонов из API.
def request_pokemons():
    cache_service = services_provider.ServicesProvider.cache_service('pokemons')
    cache = cache_service.read_cache()
    if cache is not None:
        return cache

    count = request_count()
    r = requests.get(API_ROUTE + 'pokemon?limit=' + str(count))
    if r.status_code != 200:
        raise APIRequestException('Could not request pokemons, status code: ' + str(r.status_code))
    response_data = r.json()['results']

    cache_service.write_cache(response_data)

    return response_data

# Функция для выполнения запроса и получения информации о конкретном покемоне.
def request_pokemon(pokemon_name: str):
    cache_service = services_provider.ServicesProvider.cache_service('pokemon-' + pokemon_name)
    cache = cache_service.read_cache()
    if cache is not None:
        return cache

    r = requests.get(API_ROUTE + 'pokemon/' + pokemon_name)
    if r.status_code != 200:
        raise APIRequestException('Could not request pokemon ' + pokemon_name + ', status code: ' + str(r.status_code))
    response_data = r.json()

    cache_service.write_cache(response_data)

    return response_data

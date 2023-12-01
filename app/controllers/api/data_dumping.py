import datetime
import pathlib

from flask import request, make_response

from app import services_provider
from app.pokemon_api import request_pokemon, APIRequestException
from app.ftp_service.ftp_interface import FTPErrorPermException


def api_dump_pokemons():
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
    except FTPErrorPermException:
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

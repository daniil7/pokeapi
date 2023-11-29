import requests

from tests import UnitTestResponse


class Test:

    @staticmethod
    def do():
        headers = {'Content-type': 'text/plain; charset=UTF-8'}
        request = requests.post(
                'http://localhost:5000/api/ftp/save-pokemon',
                data="PokemonThatDoNotExists",
                headers=headers,
                timeout=10
        )
        if request.status_code != 404:
            return UnitTestResponse.ERROR, 'Expected 404. Unexpected status code with wrong data '+str(request.status_code)

        request = requests.post(
                'http://localhost:5000/api/ftp/save-pokemon',
                data="bulbasaur",
                headers=headers,
                timeout=10
        )
        match request.status_code:
            case 200:
                return UnitTestResponse.SUCCESS, 'success'
            case 500:
                return UnitTestResponse.ERROR, 'Code 500. Possible FTP error '
            case 404:
                return UnitTestResponse.WARNING, 'Code 404. Could not request pokemon.'+request.text
            case _:
                return UnitTestResponse.ERROR, request.text

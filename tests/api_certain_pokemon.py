import requests

from pathlib import Path

from tests import UnitTestResponse


class Test:

    @staticmethod
    def do():
        request = requests.get('http://localhost:5000/api/pokemon/bulbasaur',
                               timeout=10)
        match request.status_code:
            case 200:
                return UnitTestResponse.SUCCESS, 'success'
            case 404:
                return UnitTestResponse.WARNING, request.json()['error']
            case _:
                return UnitTestResponse.ERROR, request.text

import requests
import jsonschema

from tests import UnitTestResponse


class Test:

    def do():
        headers = {'Content-type': 'application/json; charset=UTF-8'}
        request = requests.post(
                'http://localhost:5000/api/battle/write-result',
                json={
                    "user_pokemon": {
                        "wrong_field": "123",
                        "score": 123,
                        },
                    "wrong_field": {
                        "name": "bulbasaur",
                        "score":123,
                    },
                },
                headers=headers,
        )
        if request.status_code != 400:
            return UnitTestResponse.ERROR, 'Unexpected status code with wrong data '+str(request.status_code)

        request = requests.post(
                'http://localhost:5000/api/battle/write-result',
                json={
                    "user_pokemon": {
                        "name": "charizard",
                        "score": 1,
                        },
                    "enemy_pokemon": {
                        "name": "bulbasaur",
                        "score": 2,
                    },
                },
                headers=headers,
        )
        match request.status_code:
            case 200:
                return UnitTestResponse.SUCCESS, 'success'
            case 400:
                return UnitTestResponse.ERROR, 'Code 400 with correct data '+request.text
            case _:
                return UnitTestResponse.ERROR, request.text

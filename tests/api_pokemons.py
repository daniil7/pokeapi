import requests
import jsonschema

from tests import UnitTestResponse


class Test:

    @staticmethod
    def do():
        request = requests.get('http://localhost:5000/api/pokemon', timeout=10)
        match request.status_code:
            case 200:
                # Валидация json
                required_schema = {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'type': 'string'
                            },
                            'url': {
                                'type': 'string'
                            }
                        }
                    }
                }
                try:
                    jsonschema.validate(instance=request.json(),
                                        schema=required_schema)
                except Exception:
                    return UnitTestResponse.ERROR, 'invalid JSON schema'
                return UnitTestResponse.SUCCESS, 'success'
            case 404:
                return UnitTestResponse.WARNING, request.json()['error']
            case _:
                return UnitTestResponse.ERROR, request.text

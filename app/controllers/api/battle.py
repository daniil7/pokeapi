import jsonschema
from flask import request, make_response

from app.models import BattlesHistory
from app.database import db_session
from app.settings import CONFIG
from app import services_provider

def api_battle_write_result_route():
    # API-маршрут для записи результатов битвы.

    score = request.json

    # Валидация json
    required_schema = {
        'type': 'object',
        'properties': {
            'user_pokemon': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'score': {'type': 'number'}
                },
                "required": ["name", "score"]
            },
            'enemy_pokemon': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'score': {'type': 'number'}
                },
                "required": ["name", "score"]
            }
        },
        "required": ["user_pokemon", "enemy_pokemon"]
    }
    try:
        jsonschema.validate(instance=request.json, schema=required_schema)
    except Exception:
        return make_response({'error': 'invalid json schema', 'test': score}, 400)

    battle_result = BattlesHistory(
        score['user_pokemon']['name'],
        score['enemy_pokemon']['name'],
        score['user_pokemon']['score'],
        score['enemy_pokemon']['score'],
    )
    db_session.add(battle_result)
    db_session.commit()
    mail_service = services_provider.ServicesProvider.mail_service(CONFIG['MAIL_TO_ADDRESS'])
    mail_service.send_a_letter(
        'user pokemon: ' +
        str(score['user_pokemon']['name']) + ' ' +
        str(score['user_pokemon']['score']) + '\n' +
        'enemy pokemon: ' +
        str(score['enemy_pokemon']['name']) + ' ' +
        str(score['enemy_pokemon']['score'])
    )

    return 'success'

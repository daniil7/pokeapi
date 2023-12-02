from itsdangerous import URLSafeTimedSerializer

from app.settings import CONFIG


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(CONFIG['APP_SECRET_KEY'])
    return serializer.dumps(email, salt=CONFIG['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(CONFIG['APP_SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=CONFIG['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except Exception:
        return None
    return email

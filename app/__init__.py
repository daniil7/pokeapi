from flask import Flask
from flask_login import LoginManager
from flask import session

from app.settings import CONFIG
from app.models import User

app = Flask(__name__)

# Views

from app import views

# Database

from app import database

@app.teardown_appcontext
def shutdown_session(exception=None):
    # Закрываем соединение с БД после конца констекста запроса
    database.db_session.remove()

database.init_db()

# Sessions configuration

app.secret_key = CONFIG['APP_SECRET_KEY']

# Login manager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

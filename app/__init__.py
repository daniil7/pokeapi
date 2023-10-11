from flask import Flask

app = Flask(__name__)

from app import views
from app import database


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()

database.init_db()

from flask import abort, url_for, redirect, render_template
from flask_login import login_user, current_user

from app.oauth import OAuthSignIn
from app.models import User
from app.database import db_session


def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return render_template('login.html', error="Вы уже авторизованы!")
    oauth = OAuthSignIn.get_provider(provider)
    if oauth is not None:
        return oauth.authorize()
    return abort(404)

def oauth_callback(provider):
    if not current_user.is_anonymous:
        return render_template('login.html', error="Вы уже авторизованы!")
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        return render_template('login.html', error="Ошибка авторизации через " + provider)
    user = User.query.filter_by(provider_id=social_id).first()
    if not user:
        user = User(provider_id=social_id, username=username, email=email, password="")
        db_session.add(user)
        db_session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

from flask import abort, url_for, redirect, render_template, session, request
from flask_login import login_user, current_user
from sqlalchemy import exists as db_exists

from app.oauth import OAuthSignIn
from app.models import User
from app.database import db_session
from app.forms.authentification import AuthenticationForm
from app.forms.oauth_confirm_registration import OAuthConfirmRegistrationForm


def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return render_template('login.html', form=AuthenticationForm(), error="Вы уже авторизованы!")
    oauth = OAuthSignIn.get_provider(provider)
    if oauth is not None:
        return oauth.authorize()
    return abort(404)

def oauth_callback(provider):

    if not current_user.is_anonymous:
        return render_template('login.html', form=AuthenticationForm(), error="Вы уже авторизованы!")

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()

    if social_id is None:
        return render_template('login.html', form=AuthenticationForm(), error="Ошибка авторизации через " + provider)

    user = User.query.filter_by(provider_id=social_id).first()

    if not user:
        session['OAUTH_PROVIDER'] = provider
        session['OAUTH_ID'] = social_id
        return redirect('/oauth-confirm-registration')

    login_user(user, True)

    return redirect(url_for('index'))

def oauth_confirm_registration():
    form = OAuthConfirmRegistrationForm(request.form)

    if request.method == 'POST' and form.validate():

        if session['OAUTH_ID'] is None:
            return render_template('error_page.html', error='OAuth id отсутствует')

        if db_session.query(db_exists().where(
                    User.username == request.form.get('username'),
            )).scalar():
            return render_template('oauth_confirm_registration.html', form=form, error="Username занят")

        user = User(provider_id=session['OAUTH_ID'],
                username=form.username.data,
                email=None,
                password=None)
        db_session.add(user)
        db_session.commit()

        session['OAUTH_PROVIDER'] = None
        session['OAUTH_ID'] = None

        login_user(user, True)

        redirect(url_for('index'))

    return render_template('oauth_confirm_registration.html', form=form)

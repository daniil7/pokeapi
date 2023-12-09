import datetime

import werkzeug
from flask import redirect, request, render_template
from flask_login import login_user, logout_user
from sqlalchemy import exists as db_exists, or_ as db_or

from app import app
from app import services_provider
from app.database import db_session
from app.models import User
from app.email_token import generate_confirmation_token, confirm_token
from app.settings import CONFIG
from app.forms.registration import RegistrationForm
from app.forms.authentification import AuthenticationForm
from app.forms.reset_password_request import ResetPasswordRequestForm
from app.forms.reset_password import ResetPasswordForm


def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():

        if db_session.query(db_exists().where(
                db_or(
                    User.username == request.form.get('username'),
                    User.email == request.form.get('email')
                )
            )).scalar():
            return render_template('sign_up.html', form=form, error="Email зарегистрирован или username занят")

        user = User(username=request.form.get("username"),
                    email=request.form.get("email"))
        user.set_password(request.form.get("password"))
        db_session.add(user)
        db_session.commit()

        token = generate_confirmation_token(user.email)

        mail_service = services_provider.ServicesProvider.mail_service(mailto=user.email)
        mail_service.send_a_letter('Подтвердите регистрацию на PokeAPI. \n \
                Если вы не регистрировались, проигнорируйте это сообщение. \n' +
                CONFIG['APP_URL']+'/confirm/'+token)

        return render_template("email_confirmed.html")

    return render_template("sign_up.html", form=form)

def login():
    form = AuthenticationForm(request.form)

    if request.method == "POST" and form.validate():

        user = User.query.filter_by(
            username=request.form.get("username")).first()

        if user.password is None:
            return render_template('error_page.html', error="Авторизация через провайдера")

        if user is None or not user.check_password(request.form.get("password")):
            return render_template('login.html', form=form, error="Неверный логин или пароль")
        if not user.is_verified():
            return render_template('login.html', form=form, error="Аккаунт не подтверждён")

        token = generate_confirmation_token(user.email)
        mail_service = services_provider.ServicesProvider.mail_service(mailto=user.email)
        mail_service.send_a_letter('Перейдите по ссылке для авторизации: \n' +
            CONFIG['APP_URL']+'/second-factor/'+token)

        return render_template('second_factor.html')

    return render_template("login.html", form=form)

def reset_password_request():
    form = ResetPasswordRequestForm(request.form)

    if request.method == "GET":

        return render_template("reset_password_request.html", form=form)

    if request.method == "POST" and form.validate():

        user = User.query.filter_by(
            email=request.form.get("email")).first()

        if user is None:
            return render_template('error_page.html', error="Пользователь с таким email не найден")

        token = generate_confirmation_token(user.email)
        mail_service = services_provider.ServicesProvider.mail_service(mailto=user.email)
        mail_service.send_a_letter('Перейдите по ссылке для сброса пароля: \n' +
            CONFIG['APP_URL']+'/reset-password?token='+token)

        return render_template('error_page.html', error="Перейдите по ссылке на email для сброса пароля")

    return render_template('reset_password_request.html', form=form)

def reset_password():
    form = ResetPasswordForm(request.form)

    if request.method == "GET":

        return render_template("reset_password.html", form=form, token=request.args.get("token"))

    if request.method == "POST" and form.validate():

        email = confirm_token(request.form.get('token'), expiration=1800)

        if email is not None:
            user = User.query.filter_by(email=email).first()
            user.set_password(request.form.get('password'))
            db_session.add(user)
            db_session.commit()
            login_user(user)
        else:
            raise InvalidTokenException()
        return render_template('error_page.html', error="Пароль успешно изменён")

    return render_template('index.html')


def second_factor(token):
    email = confirm_token(token, expiration=1800)
    if email is not None:
        user = User.query.filter_by(email=email).first()
        login_user(user)
    else:
        raise InvalidTokenException()
    return render_template('second_factor.html')

def confirm_email(token):
    email = confirm_token(token, expiration=3153600000)
    if email is None:
        raise InvalidTokenException()
    user = User.query.filter_by(email=email).first()
    if user.email_verified_at is not None:
        raise AccountAlreadyConfirmedException()
    if email == user.email:
        user.email_verified_at = datetime.datetime.now()
        db_session.add(user)
        db_session.commit()
        login_user(user)
    return render_template('email_confirmed.html')

def logout():
    logout_user()
    return redirect('/')

class InvalidTokenException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Токен невалиден или просрочен.'

class AccountAlreadyConfirmedException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Аккаунт уже подтверждён.'

def TokenErrorHandler(e):
    return render_template('error_page.html', error=e.description)

app.register_error_handler(InvalidTokenException, TokenErrorHandler)
app.register_error_handler(AccountAlreadyConfirmedException, TokenErrorHandler)

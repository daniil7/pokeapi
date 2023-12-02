from wtforms import Form, StringField, PasswordField, EmailField, validators

class RegistrationForm(Form):
    username = StringField('Имя пользователя', [
        validators.DataRequired('Введите имя пользователя'),
        validators.Length(min=4, max=25)
    ])
    email = EmailField('Email адрес', [
        validators.DataRequired('Введите email адрес'),
        validators.Length(min=6, max=35),
        validators.Email('Ввелите корректный email адрес')
    ])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])
    confirm = PasswordField('Подтверждение пароля')

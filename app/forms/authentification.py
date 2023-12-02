from wtforms import Form, StringField, PasswordField, validators

class AuthenticationForm(Form):
    username = StringField('Имя пользователя', [
        validators.DataRequired('Введите имя пользователя'),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('Пароль', [
        validators.DataRequired()
    ])

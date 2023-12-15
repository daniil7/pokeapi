from wtforms import Form, StringField, PasswordField, EmailField, validators

class ResetPasswordRequestForm(Form):
    email = EmailField('Email адрес', [
        validators.DataRequired('Введите email адрес'),
        validators.Length(min=6, max=35),
        validators.Email('Введите корректный email адрес')
    ])

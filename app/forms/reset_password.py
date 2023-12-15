from wtforms import Form, PasswordField, validators

class ResetPasswordForm(Form):
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])
    confirm = PasswordField('Подтверждение пароля')

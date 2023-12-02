from wtforms import Form, StringField, validators

class OAuthConfirmRegistrationForm(Form):
    username = StringField('Имя пользователя', [
        validators.DataRequired('Введите имя пользователя'),
        validators.Length(min=4, max=25)
    ])

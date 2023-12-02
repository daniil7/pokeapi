import json

from flask import url_for, redirect, request
from rauth import OAuth2Service

from app.settings import CONFIG

class OAuthSignIn():
    providers = {}

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = CONFIG['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if not self.providers:
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        if provider_name in self.providers:
            return self.providers[provider_name]
        return None

# class VKSignIn(OAuthSignIn):
#     def __init__(self):
#         super().__init__('vk')
#         self.service = OAuth2Service(
#             name='vk',
#             client_id=self.consumer_id,
#             client_secret=self.consumer_secret,
#             authorize_url='https://oauth.vk.com/authorize',
#             access_token_url='https://oauth.vk.com/access_token',
#             base_url='https://oauth.vk.com/'
#         )
#     def authorize(self):
#         return redirect(self.service.get_authorize_url(
#             scope='email',
#             response_type='code',
#             redirect_uri=self.get_callback_url())
#         )
#     def callback(self):
#         def decode_json(payload):
#             return json.loads(payload.decode('utf-8'))
#         if 'code' not in request.args:
#             return None, None, None
#         oauth_session = self.service.get_auth_session(
#             data={'code': request.args['code'],
#                   'grant_type': 'authorization_code',
#                   'redirect_uri': self.get_callback_url()},
#             decoder=decode_json
#         )
#         me = oauth_session.get('me').json()
#         return (
#             'vk$' + me['id'],
#             me.get('email').split('@')[0],
#             me.get('email')
#         )

class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super().__init__('yandex')
        self.service = OAuth2Service(
            name='yandex',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.yandex.ru/authorize',
            access_token_url='https://oauth.yandex.ru/token',
            base_url='https://login.yandex.ru/'
        )
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            # scope='login:email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )
    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code'
            },
            decoder=decode_json
        )
        me = oauth_session.get('info').json()
        return (
            'yandex$' + me['id'],
            me['default_email'].split('@')[0],
            me['default_email']
        )

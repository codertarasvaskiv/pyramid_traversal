# -*- coding: utf-8 -*-
import binascii
from hashlib import sha512
from pyramid.authentication import BasicAuthAuthenticationPolicy, b64decode
from ConfigParser import ConfigParser


class AuthenticationPolicy(BasicAuthAuthenticationPolicy):

    def __init__(self,  debug=False):

        self.debug = debug
        config = ConfigParser()
        self.users = {
            'taras': {'name': 'admin', 'group': 'admin'},
            'taras2': {'name': 'editor', 'group': 'editor'}
        }


    def unauthenticated_userid(self, request):

        token = self._get_credentials(request)
        if token:
            user = self.users.get(token)
            if user:
                return user['name']


    def check(self, user, request):

        token = request.params.get('acc_token')
        auth_groups = ['g:{}'.format(user['group'])]

        if not token:
            token = request.headers.get('X-Access-Token')
            if not token:
                if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
                    try:
                        json = request.json_body
                    except ValueError:
                        json = None
                    token = isinstance(json, dict) and json.get('access', {}).get('token')
                if not token:
                    return auth_groups
        auth_groups.append('{}_{}'.format(user['name'], token))

        return auth_groups

    def callback(self, username, request):

        token = self._get_credentials(request)
        if token:
            user = self.users.get(token)
            if user:
                return self.check(user, request)

    def _get_credentials(self, request):
        authorization = request.headers.get('Authorization')

        if not authorization:
            return None

        username = authorization
        return username


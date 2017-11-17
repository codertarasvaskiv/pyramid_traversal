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
            'taras2': {'name': 'editor', 'group': 'editor'},
            'oleg': {'name': 'oleg', 'group': 'view_list'}
        }


    def unauthenticated_userid(self, request):

        token = self._get_credentials(request)
        if token:
            user = self.users.get(token)
            if user:
                return user['name']


    def check(self, user, request):

        token = request.params.get('acc_token')
        auth_groups = ['{}'.format(user['group'])]

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
                    print 'not token ', auth_groups
                    return auth_groups

        auth_groups.append('{}'.format(token))
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


# inside wiew is called
def authenticated_role(request):
    # principals = request.effective_principals
    # if hasattr(request, 'context'):
    #     roles = get_local_roles(request.context)
    #     local_roles = [roles[i] for i in reversed(principals) if i in roles]
    #     if local_roles:
    #         return local_roles[0]
    # groups = [g for g in reversed(principals) if g.startswith('g:')]
    print 'authenticated_role(request) is called'
    return 'taras3'
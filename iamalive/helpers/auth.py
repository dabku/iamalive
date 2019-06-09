from json import loads
from flask import request
import base64


class Auth:
    def __init__(self):
        self._auth_token_and_pwd = None
        self._auth_admin = None
        self._not_authorized = None

    def login_required(self, f):
        def decorated(*args, **kwargs):
            try:
                data = loads(request.data)['auth_data']
            except (ValueError, KeyError):
                raise self._not_authorized
            if not self._auth_token_and_pwd(device_id=kwargs.get('device_id', None),
                                            token=data.get('token', None),
                                            password=data.get('password', None),
                                            username=data.get('user', None)):
                raise NotAuthorized
            return f(*args, **kwargs)

        return decorated

    def admin_login_required(self, f):
        def decorated(*args, **kwargs):
            try:
                data = loads(request.data)['auth_data']
            except (ValueError, KeyError):
                raise self._not_authorized
            if not self._auth_admin(username=data.get('user', None), password=data.get('password', None)):
                raise NotAuthorized
            return f(*args, **kwargs)

        return decorated

    def authorize(self, f):
        self._auth_token_and_pwd = f
        return f

    def authorize_admin(self, f):
        self._auth_admin = f
        return f

    def not_authorized_exception(self, f):
        self._not_authorized = f
        return f


class AuthHeaders(Auth):

    def login_required(self, f):
        def decorated(*args, **kwargs):
            # todo: put it in try when changing tests
            user, pwd, token = self.extract_credentials_from_header(request.headers)

            if not self._auth_token_and_pwd(device_id=kwargs.get('device_id', None),
                                            token=token,
                                            password=pwd,
                                            username=user):
                raise NotAuthorized
            return f(*args, **kwargs)

        return decorated

    def admin_login_required(self, f):
        def decorated(*args, **kwargs):
            # todo: put it in try when changing tests
            user, pwd, token = self.extract_credentials_from_header(request.headers)
            if not self._auth_admin(username=user, password=pwd, token=token):
                raise NotAuthorized
            return f(*args, **kwargs)

        return decorated

    @staticmethod
    def extract_credentials_from_header(headers):
        username, password, token = None, None, None
        try:
            auth_type, auth = headers.get('Authorization').split(' ')
        except AttributeError:
            return None, None, None
        if auth_type == 'Basic':
            auth = base64.b64decode(auth)
            try:
                username, password = auth.decode("utf-8").split(':')
            except ValueError:
                return None, None, None
        elif auth_type == 'Bearer':
            token = auth
        return username, password, token


class NotAuthorized(Exception):
    pass

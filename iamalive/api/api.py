from flask import request
from flask_restful import Resource, HTTPException
from iamalive.helpers.server_helpers import extract_properties_from_dict

import json
from iamalive.api import myauth

from . import db_con


class ResourceNotFound(HTTPException):
    pass


class ResourceAlreadyInDatabase(HTTPException):
    pass


@myauth.not_authorized_exception
class NotAuthorized(HTTPException):
    pass


class InvalidCredentials(HTTPException):
    pass


class InvalidRequest(HTTPException):
    pass


custom_errors = {
    'ResourceNotFound': {
        'message': "Resource does not exist.",
        'status': 410,
    },
    'ResourceAlreadyInDatabase': {
        'message': "Resource with the same name already exists in the database.",
        'status': 409,
    },
    'NotAuthorized': {
        'message': "You are unauthorized to perform this action",
        'status': 403,
    },
    'InvalidCredentials': {
        'message': "Supplied credentials were not valid",
        'status': 401,
    },
    'InvalidRequest': {
        'message': "Supplied data is not valid",
        'status': 403,
    }
}


@myauth.authorize
def authorize(device_id=None, username=None, token=None, password=None):
    try:
        if not (db_con.is_authorized(device_id=device_id, username=username, token=token, password=password)
                or db_con.is_authorized_admin(device_id=device_id, username=username, token=token, password=password)):
            raise InvalidCredentials
    except db_con.NotInDatabase:
        raise InvalidCredentials
    return True


@myauth.authorize_admin
def authorize_admin(device_id=None, username=None, token=None, password=None):
    try:
        if not db_con.is_authorized_admin(device_id=device_id, username=username, token=token, password=password):
            raise InvalidCredentials
    except db_con.NotInDatabase:
        raise InvalidCredentials
    return True


class Pong(Resource):

    @staticmethod
    def get():
        _ = request
        return {'message': 'pong'}


class Device(Resource):

    @myauth.login_required
    def get(self, device_id):
        try:
            device = db_con.get_device(device_id)
        except db_con.NotInDatabase:
            raise ResourceNotFound
        return device

    @myauth.admin_login_required
    def post(self, device_id):
        try:
            data = json.loads(request.data)['data']
        except KeyError:
            data = {}
        try:
            db_con.add_device(device_id, data)
        except db_con.DuplicatedResource:
            raise ResourceAlreadyInDatabase
        except db_con.InvalidData:
            raise InvalidRequest('test')
        return {device_id: ''}


class DeviceList(Resource):
    @myauth.admin_login_required
    def get(self):
        flatten = (request.args.get('flatten', 'false').lower() == 'true')
        d = db_con.get_all_devices()
        for item in d:
            del item['password']
            del item['token_data']['token']
            if flatten:
                item['properties'] = extract_properties_from_dict(item['properties'])
        return [item for item in d]


class DeviceDetails(Resource):
    @myauth.login_required
    def get(self, device_id):
        try:
            data = db_con.get_device_details(device_id)
        except db_con.NotInDatabase:
            raise ResourceNotFound
        return data

    @myauth.login_required
    def post(self, device_id):
        try:
            data = json.loads(request.data)
        except KeyError:
            data = {}
        try:
            db_con.set_device_details(device_id, data)
        except db_con.NotInDatabase:
            raise ResourceNotFound
        return {device_id: 'OK'}


class DeviceToken(Resource):
    @myauth.login_required
    def get(self, device_id):
        try:
            token = db_con.get_token_device(device_id)
        except db_con.NotInDatabase:
            raise ResourceNotFound
        return {'token': token}

    @myauth.login_required
    def put(self, device_id):
        try:
            db_con.set_token(device_id)
        except db_con.NotInDatabase:
            raise ResourceNotFound
        return {device_id: 'OK'}


class DeviceStatus(Resource):
    @myauth.login_required
    def get(self, device_id):
        try:
            status = db_con.get_device_status(device_id)
        except db_con.NotInDatabase:
            raise ResourceNotFound
        return status

    @myauth.login_required
    def post(self, device_id):
        try:
            data = json.loads(request.data)
        except KeyError:
            data = {}
        try:
            db_con.set_device_status(device_id, data)
        except db_con.NotInDatabase:
            raise ResourceNotFound
        return {device_id: 'OK'}


class AuthenticateUser(Resource):
    def get(self):
        try:
            username = request.args['username']
            password = request.args['password']
        except KeyError:
            raise InvalidRequest

        try:
            authorize_admin(username=username, password=password)
        except NotAuthorized:
            raise
        token = db_con.get_token_admin(username)

        return {'token': token}

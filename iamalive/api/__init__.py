from flask_restful import Api
from iamalive.helpers.auth import AuthHeaders as Auth

myauth = Auth()

global db_con


def create_api(app):
    global db_con
    db_con = app.config['db']

    my_api = Api(app)

    from iamalive.api.api import Device, DeviceToken, DeviceDetails, DeviceList, AuthenticateUser, Pong, custom_errors
    my_api.add_resource(Pong, '/api/v1/ping')
    my_api.add_resource(Device, '/api/v1/device/<string:device_id>')
    my_api.add_resource(DeviceList, '/api/v1/device')
    my_api.add_resource(DeviceToken, '/api/v1/device/<string:device_id>/token')
    my_api.add_resource(DeviceDetails, '/api/v1/device/<string:device_id>/details')
    my_api.add_resource(AuthenticateUser, '/api/v1/authenticate')
    my_api.errors = custom_errors

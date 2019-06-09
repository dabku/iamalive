import unittest

from iamalive import create_app

from iamalive.config.config import TestsFlaskConfig
import json
from iamalive.config.config import TestsDbConfig
from copy import deepcopy
import os
import base64


class TestApi(unittest.TestCase):

    @classmethod
    def reload_database(cls):
        cls.db = cls.app.config['db']
        cls.db.load_db_data(TestsDbConfig.Data)

        db_to_model = deepcopy(TestsDbConfig.Data)

        cls.model = {data['name']: data for data in db_to_model['devices']}

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestsFlaskConfig, TestsDbConfig)
        cls.client = cls.app.test_client()
        path_to_module = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path_to_module, 'test_api_data.json'), 'r') as f:
            configuration = json.load(f)
        cls.admin_credentials = configuration['admin_credentials']
        cls.device_credentials = configuration['device_credentials']

        cls.headers = cls.getHeaders(cls.admin_credentials, cls.device_credentials)

    @staticmethod
    def getHeaders(admin_credentials, device_credentials):
        admin_encoded_valuser_valpass = base64.b64encode(str.encode('{}:{}'.format(admin_credentials['user'],
                                                                                   admin_credentials['password'])))
        invalid_admin_encoded_valuser_invalpass = base64.b64encode(
            str.encode('{}:{}'.format(admin_credentials['user'],
                                      admin_credentials['invalid_password'])))
        device_encoded_valuser_valpass = base64.b64encode(str.encode('{}:{}'.format(device_credentials['user'],
                                                                                    device_credentials['password'])))
        device_encoded_valuser_invalpass = base64.b64encode(str.encode('{}:{}'.format(device_credentials['user'],
                                                                                      device_credentials['password'])))

        headers = {'admin_bearer': {'Authorization': 'Bearer ' +
                                                     admin_credentials['token']},
                   'admin_basic': {'Authorization': 'Basic ' +
                                                    str(admin_encoded_valuser_valpass[2:-1])},
                   'device_bearer': {'Authorization': 'Bearer ' +
                                                      device_credentials['token']},
                   'device_basic': {'Authorization': 'Basic ' +
                                                     str(device_encoded_valuser_valpass)[2:-1]},

                   'invalidtoken_admin_bearer': {'Authorization': 'Bearer ' +
                                                                  admin_credentials['invalid_token']},
                   'invalidpass_admin_basic': {'Authorization': 'Basic ' +
                                                                str(invalid_admin_encoded_valuser_invalpass[2:-1])},
                   'invalidtoken_device_bearer': {'Authorization': 'Bearer ' +
                                                                   device_credentials['invalid_token']},
                   'invalidpass_device_basic': {'Authorization': 'Basic ' +
                                                                 str(device_encoded_valuser_invalpass)[2:1 - 1]}
                   }
        return headers


class TestApiFunctionalAdmin(TestApi):
    def test_pong(self):
        resp = self.client.get(path='/api/v1/ping')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['message'], 'pong')

    def test_get_devices_admin(self):
        resp = self.client.get(path='/api/v1/device', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json), 1)

    def test_get_existing_device_admin(self):
        resp = self.client.get(path='/api/v1/device/rPi2', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['name'], 'rPi2')
        self.assertFalse('properties' in resp.json)

    def test_get_non_existing_device_admin(self):
        resp = self.client.get(path='/api/v1/device/thisdevicedosenotexist', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 410)

    def test_add_device_admin(self):
        new_device = 'test_add_device'
        resp = self.client.get(path='/api/v1/device', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        device_count = len(resp.json)
        resp = self.client.post(path='/api/v1/device/{}'.format(new_device), content_type='application/json',
                                json={'data': {'password': '12345'}}, headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json[new_device], '')
        self.assertEqual(len(resp.json), 1)
        resp = self.client.get(path='/api/v1/device', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), device_count + 1)

    def test_add_duplicated_device_admin(self):
        new_device = 'rPi2'

        resp = self.client.post(path='/api/v1/device/{}'.format(new_device), content_type='application/json',
                                json={'data': {'password': '12345'}}, headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 409)

    def test_add_device_duplicated_admin(self):
        new_device = 'test_duplicated'
        resp = self.client.get(path='/api/v1/device', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        device_count = len(resp.json)
        resp = self.client.post(path='/api/v1/device/{}'.format(new_device), content_type='application/json',
                                json={'data': {'password': '12345'}}, headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json[new_device], '')
        self.assertEqual(len(resp.json), 1)

        resp = self.client.get(path='/api/v1/device', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), device_count + 1)

        resp = self.client.post(path='/api/v1/device/{}'.format(new_device), content_type='application/json',
                                json={'data': {'password': '12345'}}, headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 409)

    def test_properties_admin(self):
        resp = self.client.get(path='/api/v1/device/rPi2/details', headers=self.headers['admin_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json), 1)

    def test_add_properties_admin(self):
        path_to_module = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path_to_module, 'test_api_data.json'), 'r') as f:
            test_cases = json.load(f)['test_add_properties']
        for test_case in test_cases.values():
            resp = self.client.post(path=test_case['in']['url'], content_type='application/json', json={
                'data': {**test_case['in']['data']}}, headers=self.headers['admin_bearer'])
            self.assertEqual(resp.status_code, test_case['out']['code'])


class TestApiFunctionalsDevice(TestApi):
    def test_get_device_deviceuser(self):
        resp = self.client.get(path='/api/v1/device/rPi2', headers=self.headers['device_bearer'])
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json), 1)


class TestApiUnauthorizedActionsBearer(TestApi):

    def test_get_non_existing_device_admin_invalid_token(self):
        resp = self.client.get(path='/api/v1/device/thisdevicedosenotexist',
                               headers=self.headers['invalidtoken_admin_bearer'])
        self.assertEqual(resp.status_code, 401)

    def test_get_non_existing_device_admin_no_auth(self):
        resp = self.client.get(path='/api/v1/device/thisdevicedosenotexist',
                               headers=self.headers['invalidtoken_admin_bearer'])
        self.assertEqual(resp.status_code, 401)

    def test_get_existing_device_admin_invalid_token(self):
        resp = self.client.get(path='/api/v1/device/rPi2',
                               headers=self.headers['invalidtoken_admin_bearer'])
        self.assertEqual(resp.status_code, 401)

    def test_get_existing_device_admin_no_auth(self):
        resp = self.client.get(path='/api/v1/device/rPi2',
                               headers=self.headers['invalidtoken_admin_bearer'])
        self.assertEqual(resp.status_code, 401)

import unittest
from iamalive.db.db import IAADatabase
from iamalive.config.config import TestsDbConfig
from copy import deepcopy


class TestBase(unittest.TestCase):

    @classmethod
    def reload_database(cls):
        cls.db = IAADatabase(TestsDbConfig)
        cls.db.load_db_data(TestsDbConfig.Data)
        db_to_model = deepcopy(TestsDbConfig.Data.data_file)
        cls.model = {data['name']: data for data in db_to_model['devices']}


class TestDb(TestBase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.reload_database()

    def test_get_all_devices(self):
        result = self.db.get_all_devices()

        self.assertEqual(len(result), len(self.model))
        for item in result:
            self.assertFalse('_id' in item)
            self.assertDictEqual(item, self.model[item['name']])

    def test_get_device(self):
        result = self.db.get_device('rPi2', restricted_fields=True)
        result2 = self.db.get_device('rPi2')
        self.assertDictEqual(result, result2)
        self.assertEqual(len(IAADatabase.fields), len(result))

    def test_get_device_unrestricted(self):
        result = self.db.get_device('rPi2', restricted_fields=False)
        self.assertDictEqual(result, self.model['rPi2'])

    def test_get_device_not_in_database(self):
        self.assertRaises(IAADatabase.NotInDatabase, self.db.get_device, 'notindatabase')

    def test_get_device_proeprties(self):
        result = self.db.get_device_details('rPi2')
        self.assertDictEqual(result, self.model['rPi2']['properties'])

    def test_is_authorized(self):
        result = self.db.is_authorized('rPi2', password='password_rpi2')
        self.assertTrue(result)
        result = self.db.is_authorized('rPi2', token='rpi2_token')
        self.assertTrue(result)
        result = self.db.is_authorized('rPi2', password='invalid_password')
        self.assertFalse(result)
        result = self.db.is_authorized('rPi2', token='invalid_rpi2token')
        self.assertFalse(result)

    def test_is_authorized_admin(self):
        result = self.db.is_authorized_admin('admin', password='password_admin')
        self.assertTrue(result)
        result = self.db.is_authorized_admin('admin', password='invalid_password')
        self.assertFalse(result)


class TestDbModifiers(TestBase):

    def setUp(self):
        self.reload_database()

    def test_add_device(self):
        len1 = len(self.db.get_all_devices())
        result = self.db.add_device('new_device', {'password': 'password'})
        self.assertIsNone(result)
        len2 = len(self.db.get_all_devices())
        self.assertEqual(len1 + 1, len2)

    def test_add_device_no_password(self):
        len1 = len(self.db.get_all_devices())
        self.assertRaises(IAADatabase.InvalidData,
                          self.db.add_device,
                          'new_device',
                          {'invalid_key_password': 'password'})
        len2 = len(self.db.get_all_devices())
        self.assertEqual(len1, len2)

    def test_set_device_details(self):
        result = self.db.set_device_details('rPi2', {'storage':
                                                         {'hdd1':
                                                              {'value': 100}}})
        self.assertIsNone(result)
        properties = self.db.get_device_details('rPi2')
        self.assertEqual(properties['storage']['hdd1']['value'], 100)
        self.assertNotEqual(properties['storage']['hdd1']['timestamp'],
                            self.model['rPi2']['properties']['storage']['hdd1']['timestamp'])
        del properties['storage']['hdd1']['value']
        del properties['storage']['hdd1']['timestamp']
        model_tmp = deepcopy(self.model)
        del model_tmp['rPi2']['properties']['storage']['hdd1']['value']
        del model_tmp['rPi2']['properties']['storage']['hdd1']['timestamp']
        self.assertDictEqual(properties, model_tmp['rPi2']['properties'])

    def test_set_device_details_not_exist(self):
        self.assertRaises(IAADatabase.NotInDatabase, self.db.set_device_details,
                          'rPi2doesnotexist', {'storage':
                                                   {'hdd1':
                                                        {'value': 100}}})

    def test_get_token(self):
        current_token = self.db.get_device('rPi2', restricted_fields=False)['token_data']['token']
        result = self.db.get_token_device('rPi2')
        new_token = self.db.get_device('rPi2', restricted_fields=False)['token_data']['token']
        self.assertNotEqual(current_token, new_token)
        self.assertGreater(len(result), 5)

    def test_get_token_and_authorize(self):
        token = self.db.get_token_device('rPi2')
        result = self.db.is_authorized('rPi2', token=token)
        self.assertTrue(result)

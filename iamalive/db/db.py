from pymongo import MongoClient, DESCENDING
from iamalive.helpers.server_helpers import hash_string, create_token, extract_properties_from_dict
from time import time
from hmac import compare_digest
from copy import deepcopy

device_skeleton = {'description': '',
                   'parent': None,
                   'password': None,
                   'status':
                       {
                           'value': 'OK',
                           'timestamp': 0,
                           'minimum_update_rate': 30 * 86400
                       },
                   'token_data':
                       {
                           'token': None,
                           'expiry': -1
                       },
                   'properties': {}
                   }


class IAADatabase:
    fields = ['name', 'description', 'status']

    def __init__(self, config):

        self._client = MongoClient(config.db_host)
        self._db = self._client[config.db_name]
        self.load_db_data(config.Data)
        self._db.devices.create_index([('name', DESCENDING)])

    def load_db_data(self, data):
        data_copy = deepcopy(data.data_file)
        if data.drop_tables:
            self._db['devices'].drop()
            self._db['users'].drop()
        if data.update_tables or (len(list(self._db.devices.find(None, {"_id": 0}))) == 0):
            for item in data_copy['devices']:
                self._db.devices.insert_one(item)
        if data.update_tables or (len(list(self._db.users.find(None, {"_id": 0}))) == 0):
            for item in data_copy['users']:
                self._db.users.insert_one(item)

    def get_all_devices(self):
        return list(self._db.devices.find(None, {"_id": 0}))

    def get_device(self, device_id, restricted_fields=True):
        device = self._db.devices.find_one({"name": device_id}, {"_id": 0})
        if device is None:
            raise IAADatabase.NotInDatabase
        if restricted_fields:
            response = {field: device[field] for field in self.fields}
        else:
            response = device
        return response

    class NotInDatabase(Exception):
        pass

    class DuplicatedResource(Exception):
        pass

    class InvalidData(Exception):
        pass

    class QueryNotAcknowledgedByServer(Exception):
        pass

    def add_device(self, device_id, properties):
        try:
            _ = self.get_device(device_id)
            raise IAADatabase.DuplicatedResource
        except IAADatabase.NotInDatabase:
            pass

        new_document = dict(device_skeleton)
        new_document['name'] = device_id

        try:
            new_document['password'] = hash_string(properties['password'])
        except (KeyError, TypeError):
            raise IAADatabase.InvalidData('Password must be defined when adding new device')

        try:
            new_document['parent'] = properties['parent']
        except KeyError:
            pass
        try:
            new_document['description'] = properties['description']
        except KeyError:
            pass
        new_document['token_data']['token'] = create_token()
        result = self._db.devices.insert_one(new_document)
        if not result:
            raise IAADatabase.QueryNotAcknowledgedByServer

    def get_device_details(self, device_id):
        return self.get_device(device_id, restricted_fields=False)['properties']

    def set_device_details(self, device_id, properties):
        t = int(time())
        properties = extract_properties_from_dict(properties)
        current_properties = self.get_device_details(device_id)
        for path, value in properties:
            try:
                value['timestamp'] = int(value['timestamp'])
            except (KeyError, TypeError):
                value['timestamp'] = t
        d = self.create_update_dictionary_for_mongo(current_properties, properties)

        result = self._db.devices.update_one({'name': device_id}, {'$set': {'properties': d}})
        if not result:
            raise IAADatabase.QueryNotAcknowledgedByServer

    @staticmethod
    def create_update_dictionary_for_mongo(current_properties, properties):
        update_dict = dict(current_properties)

        for property_path, values in properties:
            current_node = update_dict
            current_last_node = current_node
            for item in property_path:
                try:
                    current_node = current_node[item]
                except KeyError:
                    current_node[item] = {}
                    current_node = current_node[item]
                current_last_node = current_node
            current_last_node.update(values)
        return update_dict

    def is_authorized(self, device_id=None, username=None, token=None, password=None):
        try:
            device = self.get_device(device_id, restricted_fields=False)
        except IAADatabase.NotInDatabase:
            return False

        if token is not None:
            if compare_digest(device['token_data']['token'], hash_string(token)):
                return True

        if password is not None:
            try:
                if compare_digest(device['password'], hash_string(password)):
                    return True
            except TypeError:
                pass
        return False

    def is_authorized_admin(self, device_id=None, username=None, token=None, password=None):
        # todo JWT auth
        if username is None:
            username = 'admin'
        user = self._db.users.find_one({"user": username}, {"_id": 0})
        if user is None:
            return False

        if token is not None \
                and compare_digest(username, user['user']) \
                and compare_digest(hash_string(token), user['token_data']['token']):
            return True
        if user is not None and password is not None \
                and compare_digest(username, user['user']) \
                and compare_digest(hash_string(password), user['password']):
            return True

        return False

    def get_token_device(self, device_id):
        token = create_token()
        hashed_token = hash_string(token)
        result = self._db.devices.update_one({'name': device_id}, {'$set': {'token_data': {'token': hashed_token}}})
        if not result:
            raise IAADatabase.QueryNotAcknowledgedByServer
        return token

    def get_token_admin(self, admin_user):
        token = create_token()
        hashed_token = hash_string(token)
        result = self._db.users.update_one({'user': admin_user}, {'$set': {'token_data': {'token': hashed_token}}})
        if not result:
            raise IAADatabase.QueryNotAcknowledgedByServer
        return token

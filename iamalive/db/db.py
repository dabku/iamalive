from pymongo import MongoClient, DESCENDING, errors
from iamalive.helpers.server_helpers import hash_string, create_token, extract_properties_from_dict
from time import time
from hmac import compare_digest
from copy import deepcopy
import json
from . import logger

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

        self._client = self._get_client(config.db_host)
        self._validate_server()
        self._db = self._client[config.db_name]
        self.load_db_data(config.Data)
        self._create_index('devices', 'name', DESCENDING)

    def _validate_server(self):
        try:
            server_info = self._client.server_info()
        except errors.ConnectionFailure as e:
            msg = 'Cannot get server info for MongoDB with message:\n{}'.format(e)
            logger.error(msg)
            raise RuntimeError(msg) from None
        logger.debug(server_info)

    @staticmethod
    def _get_client(host):
        return MongoClient(host)

    def _create_index(self, collection, field, order):
        return self._db[collection].create_index([(field, order)])

    def _insert_document(self, collection, document):
        return self._db[collection].insert_one(document)

    def _drop_collection(self, collection):
        return self._db[collection].drop()

    def _get_all_from_collection(self, collection, include_mongo_id=True):
        if include_mongo_id:
            return list(self._db[collection].find(None))
        else:
            return list(self._db[collection].find(None, {"_id": 0}))

    def _get_one_from_collection(self, collection, db_filter, include_mongo_id=True):
        if include_mongo_id:
            return self._db[collection].find_one(db_filter)
        else:
            return self._db[collection].find_one(db_filter, {"_id": 0})

    def _replace_in_one(self, collection, db_filter, new_data):
        return self._db[collection].update_one(db_filter, {'$set': new_data})

    def load_db_data(self, data):
        logger.debug('Loading data into database')
        data_copy = deepcopy(data.data_file)
        logger.debug('Dropping collections')
        if data.drop_tables:
            self._drop_collection('devices')
            self._drop_collection('users')
        else:
            logger.debug('Skipping collections drop')

        if data.update_tables or (len(self._get_all_from_collection('devices')) == 0):
            logger.debug('Loading devices')
            for item in data_copy['devices']:
                self._insert_document('devices', item)
            logger.debug('Loaded {} devices'.format(len(data_copy['devices'])))
        else:
            logger.debug('Skipping loading of the devices')

        if data.update_tables or (len(self._get_all_from_collection('users')) == 0):
            logger.debug('Loading users')
            for item in data_copy['users']:
                self._insert_document('users', item)
            logger.debug('Loaded {} users'.format(len(data_copy['users'])))
        else:
            logger.debug('Skipping loading of the users')

    def get_all_devices(self):
        return self._get_all_from_collection('devices', include_mongo_id=False)

    def get_device(self, device_id, restricted_fields=True):
        device = self._get_one_from_collection('devices', db_filter={"name": device_id}, include_mongo_id=False)
        if device is None:
            logger.error('Cannot find device {} in the database'.format(device_id))
            raise IAADatabase.NotInDatabase
        if restricted_fields:
            response = {field: device[field] for field in self.fields}
        else:
            response = device
        return response

    def add_device(self, device_id, properties):
        try:
            _ = self.get_device(device_id)
            logger.warning('Device {} already in the database'.format(device_id))
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
                logger.warning('Timestamp not found, assuming current time')
                value['timestamp'] = t
        d = self.create_update_dictionary_for_mongo(current_properties, properties)
        logger.debug('New properties for device {}\n{}'.format(device_id, json.dumps(d)))
        result = self._replace_in_one('devices', db_filter={'name': device_id}, new_data={'properties': d})

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
            logger.warning('Authentication for user {}/{} failed'.format(username, device_id))
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
        logger.warning('Authentication for user {}/{} failed'.format(username,device_id))
        return False

    def is_authorized_admin(self, device_id=None, username=None, token=None, password=None):
        # todo JWT auth
        if username is None:
            username = 'admin'
        user = self._db.users.find_one({"user": username}, {"_id": 0})
        if user is None:
            logger.warning('Authentication for user {}/{} failed'.format(username, device_id))
            return False

        if token is not None \
                and compare_digest(username, user['user']) \
                and compare_digest(hash_string(token), user['token_data']['token']):
            return True
        if user is not None and password is not None \
                and compare_digest(username, user['user']) \
                and compare_digest(hash_string(password), user['password']):
            return True
        logger.warning('Authentication for user {}/{} failed'.format(username, device_id))
        return False

    def get_token_device(self, device_id):
        token = create_token()
        hashed_token = hash_string(token)

        result = self._replace_in_one('devices',
                                      db_filter={'name': device_id},
                                      new_data={'token_data': {'token': hashed_token}})
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

    class NotInDatabase(Exception):
        pass

    class DuplicatedResource(Exception):
        pass

    class InvalidData(Exception):
        pass

    class QueryNotAcknowledgedByServer(Exception):
        pass

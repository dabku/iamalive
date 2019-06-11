import requests
import base64
import random
from time import sleep
from time import time

api_url = 'http://127.0.0.1:5000'


def get_admin_token():
    params = {'username': 'admin', 'password': 'password'}
    resp = requests.get(url=api_url + '/api/v1/authenticate', params=params)
    token_from_api = resp.json()['token']
    return token_from_api


def get_header_bearer(token_for_auth):
    header = {'Authorization': 'Bearer ' + token_for_auth}
    return header


def list_devices(admin_token):
    header = get_header_bearer(admin_token)
    resp = requests.get(url=api_url + '/api/v1/device', headers=header)
    devices_from_api = resp.json()
    return devices_from_api


def add_device(admin_token):
    header = get_header_bearer(admin_token)
    resp = requests.post(url=api_url + '/api/v1/device/{}'.format('DemoDevice'),
                         json={'data': {'password': '12345'},
                               'properties': {'temperature': {'value': 0}}}, headers=header)
    return resp.status_code


def update_property(device_properties, device_token):
    header = get_header_bearer(device_token)
    resp = requests.post(url=api_url + '/api/v1/device/DemoDevice/details', headers=header, json=device_properties)
    return resp


def update_status(device_status, device_token):
    header = get_header_bearer(device_token)
    resp = requests.post(url=api_url + '/api/v1/device/DemoDevice/status', headers=header, json=device_status)
    return resp


def get_token_device():
    userpass = base64.b64encode(str.encode('{}:{}'.format('DemoDevice', '12345')))
    header = {'Authorization': 'Basic ' + str(userpass)[2:-1]}
    resp = requests.get(url=api_url + '/api/v1/device/DemoDevice/token', headers=header)
    token_from_api = resp.json()['token']
    return token_from_api


print('Logging in as an admin')
token = get_admin_token()
print('Admin token: {}'.format(token))

print('Obtaining list of current devices from API')
devices = list_devices(token)
print('Devices:\n{}'.format(devices))

# We want to prevent from attempting to add the same device twice if script was run multiple times
devices_in_db = [item['name'] for item in devices]
if 'DemoDevice' not in devices_in_db:
    print('DemoDevice not found, adding to the database')
    response_code = add_device(token)
    print('Response code (200 if success): {}'.format(response_code))
else:
    print('DemoDevice is already in the database! Skipping...')

print('Logging in as a device')
token = get_token_device()
print('Device token: {}'.format(token))

# we will put those into DemoDevice
properties_to_initalize = {
    'temperature1': {
        'value': 0,
        'threshold': 50},
    'temperature2': {
        'value': 0,
        'threshold': 50},
    'temperature3': {
        'value': 0,
        'threshold': 50},
    'temperature4': {
        'value': 0,
        'threshold': 50}
}

print('Pushing blank properties into the device')
response_code = update_property(properties_to_initalize, token)
print('Response code (200 if success): {}'.format(response_code))

# Device needs to update all properties to easily accomodate to the design
# IAA currently does not care about the history
# Note that if you want to set old timestamp, you need to specify it:
properties_to_update = {
    'temperature1': {
        'value': 0},
    'temperature2': {
        'value': 0},
    'temperature3': {
        'value': 0},
    'temperature4': {
        'value': 0,
        'timestamp': int(time()) - 60 * 60 * 24 * 1000}
}

# extract names of the properties
keys_to_update = list(properties_to_initalize.keys())
# status list
general_status = [{'value': 'OK'},
                  {'value': 'ERROR'},
                  {'value': 'custom message'},
                  {'value': 'OK', 'timestamp': int(time()) - 86400 * 365}]
try:
    while True:
        sleep(7)
        # choose random property
        key_to_update = keys_to_update[random.randint(0, len(keys_to_update) - 1)]
        # choose random value
        value = random.randint(0, 100)
        # modify poprerty dict
        properties_to_update[key_to_update]['value'] = value
        # update properties
        update_property(properties_to_update, token)
        # pick a new status
        status = general_status[random.randint(0, len(general_status) - 1)]
        # update status
        update_status(status, token)
        print('Property {} of DemoDevice was set to {} with general status: {}'.format(key_to_update, value, status))
except KeyboardInterrupt:
    pass

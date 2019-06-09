# if compiled it will be hidden
from time import time
from iamalive.helpers.server_helpers import hash_string

data = {
    "users": [
        {
            "user": "admin",
            "password": hash_string("password"),
            "token_data": {
                "token": hash_string("admin_token"),
                "expiry": -1,
                "set": int(time())
            },
        }],
    "devices": []
}

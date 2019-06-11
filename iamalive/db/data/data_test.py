from iamalive.helpers.server_helpers import hash_string

data = {
    "users": [
        {
            "user": "admin",
            "password": hash_string("password_admin"),
            "token_data": {
                "token": hash_string("admin_token"),
                "expiry": -1
            }
        }],
    "devices": [
        {
            "name": "rPi2",
            "description": "raspberry",
            "parent": None,
            "password": hash_string("password_rpi2"),
            "status": {
                "value": "OK",
                "timestamp": 123,
                "minimum_update_rate": 86400
            },
            "token_data": {
                "token": hash_string("rpi2_token"),
                "expiry": -1
            },
            "properties": {
                "storage": {
                    "hdd1": {
                        "value": 98.1,
                        "timestamp": 123,
                        "threshold": 75.0
                    },
                    "hdd2": {
                        "value": 22.1,
                        "timestamp": 124,
                        "threshold": 75.0
                    }
                },
                "others": {
                    "temperature": {
                        "value": 50.1,
                        "timestamp": 125,
                        "threshold": 100
                    }
                }
            }
        },
        {
            "name": "script",
            "password": hash_string("password_script"),
            "token_data": {
                "token": hash_string("scripttoken"),
                "expiry": 1234
            },
            "status": {
                "value": "OK_script",
                "timestamp": 123,
                "minimum_update_rate": 86400
            },
            "properties": {}
        }
    ]
}

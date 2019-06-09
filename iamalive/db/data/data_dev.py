# if compiled it will be hidden
from iamalive.helpers.server_helpers import hash_string
from time import time

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
    "devices": [
        {
            "name": "rPi2",
            "description": "Raspberry Home",
            "password": hash_string("rpi2_password"),
            "status": {
                "value": "OK",
                "timestamp": int(time()) - 3600,
                "minimum_update_rate": 86400
            },
            "token_data": {
                "token": hash_string("rpi2token"),
                "expiry": int(time()) + 8600,
                "set": int(time())
            },
            "properties": {
                "storage": {
                    "hdd1": {
                        "value": 60.1,
                        "timestamp": int(time()) - 1324,
                        "threshold": 75.0
                    },
                    "hdd2": {
                        "value": 22.1,
                        "timestamp": int(time()) - 2123,
                        "threshold": 75.0
                    }
                },
                "others": {
                    "temperature": {
                        "value": 50.1,
                        "timestamp": int(time()) - 3123,
                        "threshold": 100
                    }
                }
            }
        },
        {
            "name": "My Script",
            "description": "Script that checks data",
            "password": hash_string("script_password"),
            "token_data": {
                "token": hash_string("script_token"),
                "expiry": int(time()) + 8600,
                "set": int(time())
            },
            "status": {
                "value": "OK",
                "timestamp": int(time()) - 2 * 3600,
                "minimum_update_rate": 3600
            },
            "properties": {}
        },
        {
            "name": "NAS",
            "description": "NEtwork Attached Storage",
            "password": hash_string("nas_password"),
            "token_data": {
                "token": hash_string("nas_token"),
                "expiry": int(time()) + 8600,
                "set": int(time())
            },
            "status": {
                "value": "OK",
                "timestamp": int(time()) - 2 * 3600,
                "minimum_update_rate": 3600
            },
            "properties": {
                "temperature": {
                    "value": 22.1,
                    "timestamp": int(time()) - 8600,
                    "threshold": 100
                },
                "storage_1": {
                    "value": 93.1,
                    "timestamp": int(time()) - 8600,
                    "threshold": 90
                },
                "storage_2": {
                    "value": 92.1,
                    "timestamp": int(time()) - 8600,
                    "threshold": 90
                },
                "storage_4": {
                    "value": 91.1,
                    "timestamp": int(time()) - 8600,
                    "threshold": 90
                },
            }
        },
        {
            "name": "My Computer backup",
            "description": "Script that checks data",
            "password": hash_string("nas_password"),
            "token_data": {
                "token": hash_string("nas_token"),
                "expiry": int(time()) + 8600,
                "set": int(time())
            },
            "status": {
                "value": "On Hold",
                "timestamp": int(time()) - 4213,
                "minimum_update_rate": 86400
            },
            "properties": {}
        },
        {
            "name": "My laptop",
            "description": "Monitoring of my laptop",
            "password": hash_string("nas_password"),
            "token_data": {
                "token": hash_string("nas_token"),
                "expiry": int(time()) + 8600,
                "set": int(time())
            },
            "status": {
                "value": "OK",
                "timestamp": int(time()) - 4213,
                "minimum_update_rate": 86400
            },
            "properties": {
                "temperatures": {
                    "CPU": {
                        "value": 50.1,
                        "timestamp": int(time()) - 3123,
                        "threshold": 70
                    },
                    "HDD": {
                        "value": 50.1,
                        "timestamp": int(time()) - 3123,
                        "threshold": 40
                    }
                },
                "storage": {
                    "hdd1": {
                        "value": 60.1,
                        "timestamp": int(time()) - 1324,
                        "threshold": 75.0
                    },
                    "hdd2": {
                        "value": 22.1,
                        "timestamp": int(time()) - 22 * 86400,
                        "threshold": 75.0
                    }
                }
            }
        }
    ]
}

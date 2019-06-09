from flask import Flask
from flask_cors import CORS

import iamalive.api
from iamalive.web import create_web
from iamalive.db.db import IAADatabase


def create_app(flask_config, db_config):
    app = Flask(__name__)
    app.config.from_object(flask_config)
    CORS(app)
    app.secret_key = 'v3ra9Hkby4eFUdodr4nPLD_VeIDS6h82'
    db = IAADatabase(db_config)

    app.config['db'] = db

    iamalive.api.create_api(app)
    create_web(app)

    return app

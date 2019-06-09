import sys
from iamalive import create_app
from iamalive.config.config import getFlaskConfig, getDbConfig

if __name__ == '__main__':
    try:
        env_flask = sys.argv[1]
    except IndexError:
        env_flask = 'prod'

    try:
        env_db = sys.argv[2]
    except IndexError:
        env_db = env_flask

    dbconf = getDbConfig(env_db)
    flaskconf = getFlaskConfig(env_flask)

    app = create_app(flask_config=flaskconf, db_config=dbconf)
    app.run()

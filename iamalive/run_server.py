import sys
from iamalive import create_app
from iamalive.config.config import get_flask_config, get_db_config

if __name__ == '__main__':
    try:
        env_flask = sys.argv[1]
    except IndexError:
        env_flask = 'prod'

    try:
        env_db = sys.argv[2]
    except IndexError:
        env_db = env_flask

    dbconf = get_db_config(env_db)
    flaskconf = get_flask_config(env_flask)

    app = create_app(flask_config=flaskconf, db_config=dbconf)
    app.run(host=flaskconf.SOCKET)

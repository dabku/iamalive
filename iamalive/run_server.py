import sys
from os import path, makedirs
from iamalive import create_app
from iamalive.config.config import get_flask_config, get_db_config
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    debug_modules = [('iaa_db', logging.WARNING),
                     ('werkzeug', logging.ERROR),
                     ('urllib3', logging.ERROR)]

    script_dir = path.dirname(path.realpath(sys.argv[0]))
    if not path.exists(path.join(script_dir, 'log')):
        makedirs(path.join(script_dir, 'log'))
    log = logging.getLogger(__name__)
    for module, level in debug_modules:
        if level is None:
            continue
        log = logging.getLogger(module)
        log.propagate = False
        handler = RotatingFileHandler(path.join(script_dir, 'log', 'iaa_log.txt'), maxBytes=1048576, backupCount=5)

        formatter = logging.Formatter(
            '%(asctime)s%(levelname)8s()|%(filename)s:%(lineno)s - %(funcName)s() - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(level)
    return log


if __name__ == '__main__':

    logger = setup_logger()
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

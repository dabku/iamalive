from enum import Enum
import os

from iamalive.db.data.data_dev import data as dev_data
from iamalive.db.data.data_production import data as prod_data
from iamalive.db.data.data_test import data as test_data

path = os.path.dirname(os.path.dirname(__file__))


class ENV(Enum):
    PROD = 'prod'
    TEST = 'test'
    DEV = 'dev'
    DEMO = 'demo'


class FlaskBaseConfig:
    DEBUG = False
    SOCKET = '127.0.0.1'


class DevelopmentFlaskConfig(FlaskBaseConfig):
    DEBUG = True


class TestsFlaskConfig(FlaskBaseConfig):
    DEBUG = True


class ProductionFlaskConfig(FlaskBaseConfig):
    SOCKET = '0.0.0.0'


class DockerDemoFlaskConfig(FlaskBaseConfig):
    DEBUG = True
    SOCKET = '0.0.0.0'


class DbBaseConfig:
    pass


class DevelopmentDbConfig:
    db_host = 'localhost'
    db_name = 'iamalive_dev'

    class Data:
        data_file = dev_data
        drop_tables = False
        update_tables = False


class DockerDemoDbConfig:
    db_host = 'iaa_mongodb'
    db_name = 'iamalive_demo'

    class Data:
        data_file = dev_data
        drop_tables = True
        update_tables = True


class TestsDbConfig:
    db_host = 'localhost'
    db_name = 'iamalive_test'

    class Data:
        data_file = test_data
        drop_tables = True
        update_tables = True


class ProductionDbConfig:
    pass


def get_flask_config(environment):
    if ENV.PROD is ENV(environment) or ENV.DEMO is ENV(environment):
        return ProductionFlaskConfig
    if ENV.TEST is ENV(environment):
        return TestsFlaskConfig
    if ENV.DEV is ENV(environment):
        return DevelopmentFlaskConfig
    if ENV.DEMO is ENV(environment):
        return DockerDemoFlaskConfig
    return ProductionFlaskConfig


def get_db_config(environment):
    if ENV.PROD is ENV(environment):
        return DevelopmentDbConfig
    if ENV.TEST is ENV(environment):
        return TestsFlaskConfig
    if ENV.DEV is ENV(environment):
        return DevelopmentDbConfig
    if ENV.DEMO is ENV(environment):
        return DockerDemoDbConfig
    return ProductionDbConfig

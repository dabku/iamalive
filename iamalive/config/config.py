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


class DevelopmentFlaskConfig(FlaskBaseConfig):
    DEBUG = True


class TestsFlaskConfig(FlaskBaseConfig):
    DEBUG = True


class ProductionFlaskConfig(FlaskBaseConfig):
    pass


class DbBaseConfig:
    pass


class DevelopmentDbConfig:
    db_host = 'localhost'
    db_name = 'iamalive_dev'

    class Data:
        data_file = dev_data
        drop_tables = False
        update_tables = False


class DemoDbConfig:
    db_host = 'localhost'
    db_name = 'iamalive_dev'

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


def getFlaskConfig(enviroment):
    if ENV.PROD is ENV(enviroment) or ENV.DEMO is ENV(enviroment):
        return ProductionFlaskConfig
    if ENV.TEST is ENV(enviroment):
        return TestsFlaskConfig
    if ENV.DEV is ENV(enviroment):
        return DevelopmentFlaskConfig
    return ProductionFlaskConfig


def getDbConfig(enviroment):
    if ENV.PROD is ENV(enviroment):
        return DevelopmentDbConfig
    if ENV.TEST is ENV(enviroment):
        return TestsFlaskConfig
    if ENV.DEV is ENV(enviroment):
        return DevelopmentDbConfig
    if ENV.DEMO is ENV(enviroment):
        return DemoDbConfig
    return ProductionDbConfig

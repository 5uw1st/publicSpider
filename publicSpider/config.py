# coding:utf-8

import logging
import os
from publicSpider import BASE_PATH


def get_env(key, default):
    return os.environ.get(key, default)


class BaseConfig(object):
    DEBUG = False

    # log config
    LOG_PATH = get_env("LOG_PATH", default="/var/log/publicSpider")
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s[%(lineno)s]: %(message)s"

    # redis config
    REDIS_URI = "redis://127.0.0.1:6379/0"

    # mongodb config
    MONGODB_URI = "mongodb://127.0.0.1:27017/publicSpider"

    # id card redis key prefix
    ID_CARD_KEY_PREFIX = "ID_CARD_{0}"


class DevConfig(BaseConfig):
    DEBUG = True

    LOG_PATH = get_env("LOG_PATH", os.path.join(BASE_PATH, "logs"))
    LOG_LEVEL = logging.DEBUG


class DemoConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


CONFIG_DICT = {
    "DEV": DevConfig,
    "DEMO": DemoConfig,
    "PROD": ProdConfig
}

current_mode = get_env("ENV_MODE", default="DEV").upper()
current_config = CONFIG_DICT.get(current_mode)
if current_config is None:
    raise KeyError("ENV MODE IS NOT EXISTED!")

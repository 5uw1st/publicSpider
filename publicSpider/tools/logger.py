#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file:logger.py
@time: 2019/1/6
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from publicSpider.config import current_config


def get_logger(name, level=None):
    log_format, log_path, log_level = current_config.LOG_FORMAT, current_config.LOG_PATH, current_config.LOG_LEVEL
    logger = logging.getLogger(name)
    if len(logger.handlers) == 2:
        return logger
    logger_file = os.path.join(log_path, "{0}.log".format(name))

    logging_format = logging.Formatter(log_format)

    logger_level = level or log_level

    file_handler = TimedRotatingFileHandler(logger_file, when="D", backupCount=30)
    file_handler.setLevel(logger_level)
    file_handler.setFormatter(logging_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)
    console_handler.setFormatter(logging_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logger_level)
    return logger

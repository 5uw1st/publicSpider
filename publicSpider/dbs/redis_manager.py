#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file:redis_manager.py
@time: 2019/1/6
"""

import redis

from publicSpider.config import current_config
from publicSpider.tools.logger import get_logger

default_logger = get_logger(name="redis_client")


class RedisClient(object):
    """
    redis连接客户端
    """

    def __init__(self, logger=None):
        self.logger = logger or default_logger
        self._conn = None

    def init(self):
        self._get_conn()

    def _get_conn(self):
        if not self._conn:
            self.logger.info("Get redis connection from: {0}".format(current_config.REDIS_URI))
            self._conn = redis.from_url(url=current_config.REDIS_URI)
        return self._conn

    @property
    def conn(self):
        return self._get_conn()

    def __getattr__(self, item):
        return getattr(self._conn, item)


redis_pool = RedisClient()
redis_pool.init()

if __name__ == '__main__':
    print(redis_pool.keys("*"))

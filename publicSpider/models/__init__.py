#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file: __init__.py.py
@time: 2019/01/02
"""

from publicSpider.config import current_config
from mongoengine import connect

# connect mongodb
connect(host=current_config.MONGODB_URI)

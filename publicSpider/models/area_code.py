#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file: __init__.py.py
@time: 2019/01/02
"""
from datetime import datetime

from mongoengine import Document, StringField, IntField, DateTimeField


class AreaCodeInfo(Document):
    """
    行政区代码信息
    """
    type = StringField(max_length=20, required=True)
    name = StringField(max_length=30, required=True)
    code = IntField(required=True)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)

    def __str__(self):
        return "<{2},{0}:{1}|0x{3:0x}>".format(self.code, self.name, self.__class__.__name__, id(self))

    meta = {
        "auto_create_index": False,
        "collection": "BaseData.AreaCodeInfo",
        "ordering": ['-update_time'],
        "strict": False,
    }

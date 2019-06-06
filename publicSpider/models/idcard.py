#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file:idcard.py
@time: 2019/1/6
"""

from datetime import datetime

from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField


class IdCardInfo(Document):
    """
    身份证信息
    """
    province = StringField(max_length=30, required=True)
    city = StringField(max_length=30, required=True)
    area = StringField(max_length=30, required=True)
    name = StringField()
    sexes = IntField(choices=[0, 1])
    code = StringField(max_length=18, required=True)
    valid = BooleanField(default=False)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)

    @property
    def birth(self):
        return datetime.strptime(self.code[6:14], format="%Y%m%d").strftime("%Y-%m-%d")

    @property
    def age(self):
        now_date = datetime.now()
        birth = self.code[6:14]
        birth_date = datetime.strptime(birth, format="%Y%m%d")
        years = (now_date - birth_date).days / 365
        return years

    @property
    def sex(self):
        return "男" if self.sexes == 0 else "女"

    def __str__(self):
        return "<{0},{1}:{2}-{3}-{4}|0x{5:0x}>".format(self.__class__.__name__, self.code, self.province, self.city,
                                                       self.area, id(self))

    meta = {
        "auto_create_index": False,
        "collection": "BaseData.IdCardInfo",
        "ordering": ['-update_time'],
        "strict": False,
    }

#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file: __init__.py.py
@time: 2019/01/02
"""
import os
import time
import uuid
from hashlib import md5
from json import load as json_load, dump as json_dump

import requests

from publicSpider import DATA_PATH


def get_time(length=13):
    ct = time.time()
    return int(ct * 1000 if length == 13 else ct)


def get_uuid():
    return str(uuid.uuid1())


def get_md5(content):
    if isinstance(content, str):
        content = content.encode()
    return md5(content).hexdigest()


def load_data_from_json_file(filename):
    """
    加载json文件
    :param filename: str 文件名
    :return: obj
    """
    file_path = os.path.join(DATA_PATH, filename)
    with open(file_path, "r") as f:
        return json_load(fp=f)


def dump_data_to_json_file(data_obj, filename):
    """
    保存json对象到文件
    :param data_obj: obj 数据对象
    :param filename: str 文件名
    :return: obj
    """
    file_path = os.path.join(DATA_PATH, filename)
    with open(file_path, "w") as f:
        json_dump(obj=data_obj, fp=f)
    return data_obj


def download(url, method="GET", data=None, proxy=None, ret_type="json", **kwargs):
    """
    下载
    :param url: str 请求url
    :param method: str 请求方法
    :param data: dict 请求数据
    :param proxy: dict 代理信息
    :param ret_type: str 返回数据类型
    :param kwargs: dict 其它参数
    :return:
    """
    method = method.upper() or "GET"
    request = requests.get if method == "GET" else requests.post
    response = request(url, data=data, proxies=proxy, verify=False, **kwargs, )
    status_code = response.status_code
    if ret_type.lower() == "resp":
        result = response
    elif ret_type.lower() == "json":
        result = response.json()
    elif ret_type.lower() == "bytes":
        result = response.content
    else:
        result = response.text
    return result

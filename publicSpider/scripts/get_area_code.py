#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file:get_area_code.py
@time: 2019/01/02
"""
from collections import defaultdict
from re import compile as re_compile
from publicSpider.tools.logger import get_logger
from json import loads as json_loads
from publicSpider.models.area_code import AreaCodeInfo
from publicSpider.tools.utils import download, dump_data_to_json_file, load_data_from_json_file

logger = get_logger(name="area_code")
reg_province = re_compile(r'var json = ([\s\S]+?);')


def get_province_info():
    """
    获取省信息
    :return: dict {110000: "北京市"}
    """
    url = "http://xzqh.mca.gov.cn/fuzzySearch"
    html = download(url, ret_type="text")
    json_str = reg_province.search(html).group(1)
    json_data = json_loads(json_str)
    return {int(dt["quHuaDaiMa"]): dt["shengji"] for dt in json_data if dt["quHuaDaiMa"]}


def get_city_info(province_name="吉林省(吉)"):
    """
    获取市
    :param province_name: str 省名
    :return: dict {111000: "海淀区"}
    """
    url = "http://xzqh.mca.gov.cn/selectJson"
    data = {"shengji": province_name}
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "http://xzqh.mca.gov.cn",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "xzqh.mca.gov.cn",
    }
    ret_data = download(url, method="POST", data=data, headers=headers, ret_type="json")
    return {int(dt['quHuaDaiMa']): dt["diji"].strip() for dt in ret_data if dt['quHuaDaiMa']}


def get_area_info(province_name="浙江省(浙)", city_name="湖州市"):
    """
    获取行政区
    :param province_name: str 省名
    :param city_name: str 城市名
    :return: dict {code: name}
    """
    url = "http://xzqh.mca.gov.cn/selectJson"
    data = {"shengji": province_name, "diji": city_name}
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "xzqh.mca.gov.cn",
    }
    ret_data = download(url, method="POST", data=data, headers=headers, ret_type="json")
    return {int(dt['quHuaDaiMa']): dt["xianji"].strip() for dt in ret_data if dt['quHuaDaiMa']}


def save_data_to_mongodb(filename=None, data=None):
    """
    将数据保存到mongodb
    :param filename: str 文件名
    :param data: dict 数据对象
    :return: dict
    """
    logger.info("Start save data to mongodb")
    if filename and isinstance(filename, str):
        data = load_data_from_json_file(filename=filename)
    for dtype, dinfo in data.items():
        for code, value in dinfo.items():
            info = {
                "type": dtype,
                "name": value,
                "code": int(code)
            }
            AreaCodeInfo(**info).save()
    logger.info("Save data to mongodb finish!")


def start():
    logger.info("  Start ".center(60, "*"))
    code_info = defaultdict(dict)
    province_info = get_province_info()
    code_info["province"] = province_info
    for _, province_name in province_info.items():
        logger.info("[+]Start get city info: {0} ==> {1}".format(province_name, _))
        city_info = get_city_info(province_name)
        code_info["city"].update(city_info)
        for __, city_name in city_info.items():
            logger.info("[+]Start get area info: {0} ===>>> {1}".format(city_name, __))
            area_info = get_area_info(province_name, city_name)
            code_info["area"].update(area_info)

    # save data to json file
    filename = "area_code.json"
    dump_data_to_json_file(data_obj=code_info, filename=filename)
    # save data to mongodb
    save_data_to_mongodb(data=code_info)

    logger.info("  Finish ".center(60, "*"))


if __name__ == '__main__':
    start()

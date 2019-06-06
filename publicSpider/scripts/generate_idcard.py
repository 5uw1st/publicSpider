#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author:5uwst
@file: generate_idcard.py
@time: 2019/01/06
"""
from datetime import datetime, timedelta

from publicSpider.config import current_config
from publicSpider.dbs.redis_manager import redis_pool
from publicSpider.models.area_code import AreaCodeInfo
from publicSpider.models.idcard import IdCardInfo
from publicSpider.tools.logger import get_logger
from publicSpider.tools.utils import load_data_from_json_file

logger = get_logger(name="id_card")

WEIGHT = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
CHECK_CODE = {
    '0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7',
    '6': '6', '7': '5', '8': '5', '9': '3', '10': '2'}  # 校验码映射


def get_check_code(code17):
    """
    计算校验码
    :param code17: str 前17位身份证号
    :return: str 18位身份证号
    """
    logger.info("17 code: {0}".format(code17))
    num = 0
    for i in range(0, len(code17)):
        num += int(code17[i]) * WEIGHT[i]
    check_code = CHECK_CODE[str(num % 11)]
    logger.info("check code: {0}".format(check_code))
    return check_code


def is_leap_year(year):
    """
    判断是否是闰年
    :param year: int 年
    :return: bool
    """
    if not year % 4 and year % 100 or not year % 400:
        return True
    return False


def generate_years(start_year=1920, end_year=2010):
    """
    生成年列表
    :param start_year: 开始时间
    :param end_year: 结束时间
    :return: list
    """
    return range(start_year, end_year + 1)


def generate_year_days(year=2018):
    """
    生成一年中所有的天
    :param year: int 年
    :return: list
    """
    format_str = "%Y%m%d"
    start_date = datetime.strptime("{0}0101".format(year), format_str)
    days = 366 if is_leap_year(year) else 365
    for i in range(days):
        day_date = start_date + timedelta(days=i)
        if day_date.year == year:
            yield day_date.strftime(format_str)


def generate_sequence_code():
    """
    生成顺序码(3位)
    :return: list
    """
    return ("{0:03d}".format(i) for i in range(1, 1000))


def get_area_code():
    """
    获取行政区代码
    :return: list
    """
    area_codes = AreaCodeInfo.objects(type="area").all()
    ret = (area.code for area in area_codes)
    # ret.sort()
    return ret


area_code_info = load_data_from_json_file(filename="area_code.json")
turn_fun_dict = {
    "province": lambda x: x // 10000 * 10000,
    "city": lambda x: x // 100 * 100,
    "area": lambda x: x
}


def get_name_by_code(code, ntype="province"):
    code_info = area_code_info.get(ntype, {})
    key = turn_fun_dict[ntype](int(code))
    return code_info[str(key)]


def start():
    logger.info(" Start generate id card ".center(60, "*"))
    # get area code
    for area_code in get_area_code():
        # get year
        for year in generate_years():
            # get birth day
            for birth_day in generate_year_days(year=year):
                # get sequence code
                for seq_code in generate_sequence_code():
                    logger.debug("===>area_code:{0}, birth:{1}, seq_code:{2}".format(area_code, birth_day, seq_code))
                    # get check code:
                    id17 = "{0}{1}{2}".format(area_code, birth_day, seq_code)
                    check_code = get_check_code(code17=id17)
                    id_card = "{0}{1}".format(id17, check_code)
                    key = current_config.ID_CARD_KEY_PREFIX.format(str(area_code)[:2])
                    if not redis_pool.sismember(key, id_card):
                        redis_pool.sadd(key, id_card)
                    else:
                        logger.debug("This id card is existed, key:{0}, card:{1}".format(key, id_card))
                        continue
                    sexes = 1 - int(id_card[-2]) % 2
                    logger.info("===>Generate id card: {0}, sex: {1}".format(id_card, sexes))
                    province = get_name_by_code(code=area_code, ntype="province")
                    city = get_name_by_code(code=area_code, ntype="city")
                    area = get_name_by_code(code=area_code, ntype="area"),
                    logger.debug(
                        "===>province:{0}, city:{1}, area:{2}, birth:{3}".format(province, city, area, birth_day))
                    info = {
                        "province": province,
                        "city": city,
                        "area": area,
                        "sexes": sexes,
                        "code": id_card
                    }
                    IdCardInfo(**info).save()
    logger.info(" Finish generate id card ".center(60, "*"))


if __name__ == '__main__':
    start()

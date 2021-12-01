# coding: utf-8
# Author：quzard
import datetime
import sys
import time
import traceback
from time import sleep

from numpy import random

from Tui import *
from get_location import get_location
from read_inform import read_inform
from seu_clockin import seu_clockin

if __name__ == '__main__':
    inform = read_inform()
    username = inform.seu['username']
    password = inform.seu['password']
    name = inform.seu['name']
    enable_gps = inform.gps_inform['enable_gps']
    LAT = inform.gps_inform['LAT']  # 纬度
    LON = inform.gps_inform['LON']  # 经度
    serverchan = inform.serverchan
    ak = inform.api['ak']
    sk = inform.api['sk']
    try:
        sleep(random.uniform(5, 15))
        date_time = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        print("时间:", date_time)
        # 获取伪造地址
        if int(enable_gps) == 1 and float(LON) != 0 and float(LAT) != 0:
            result, json_data = get_location(LAT=LAT, LON=LON, ak=ak, sk=sk)
            if result:
                province = json_data['result']['addressComponent']['province']
                city = json_data['result']['addressComponent']['city']
                district = json_data['result']['addressComponent']['district']
            else:
                province = ''
                city = ''
                district = ''
        else:
            province = ''
            city = ''
            district = ''

        res = seu_clockin(username, password, province, city, district, LAT, LON)
        if res == "打卡成功!":
            person_msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n\n体温上报成功' + '\n\n' + "伪造地址：" + province + city + district
            server_post(name + '\t' + '体温上报\t成功', person_msg, serverchan)
        else:
            person_msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n\n' + res + '\n\n' + "伪造地址：" + province + city + district
            server_post(name + '\t' + '体温上报\t失败', person_msg, serverchan)
            sys.exit(1)

    except Exception as e:
        print(traceback.format_exc())
        server_post(name + '\t' + '体温上报\t失败', e, serverchan)
        sys.exit(1)

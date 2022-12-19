#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : generate_data.py
Description      : 生成随机数据
Time             : 2022/03/07 17:44:34
Author           : AllenLuo
Version          : 1.0
'''


import time
import random
from tools import logger
from faker import Faker 

fake = Faker(locale='zh_CN') 
create_date = time.strftime('%Y%m%d', time.localtime(time.time()))
appno = f'autotest-{create_date}-{random.randint(1000,9999)}'

config_dict = {"channelNo": "CUP CAR LOAN_YIXIN", "appNo": appno, "certNo": fake.ssn(min_age=18, max_age=60),
              "nameValue": f"自动化测试{random.randint(1000,9999)}",
              "loanAmount": f"{random.randint(10000,99999)}", "productType": random.choice(['11', '13']),
              "mobileNo": f"199{random.randint(10000000,99999999)}"
              }

logger.debug(f"生成的测试数据-{config_dict}")

if __name__ == '__main__':

    print(config_dict)
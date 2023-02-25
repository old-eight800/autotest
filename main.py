#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : main.py
Description      : 
Time             : 2022/12/17 18:26:52
Author           : AllenLuo
Version          : 1.0
'''


import os
import pytest
from tools import logger, BASE_DIR
import time


def start_autotest():
    logger.remove()
    create_date = time.strftime('%Y_%m_%d', time.localtime(time.time()))
    logger.add(f'log/{create_date}.log', enqueue=True, encoding='utf-8', retention=30)
    logger.info("""

     _   _   _ _____ ___    _____ _____ ____ _____ 
    / \ | | | |_   _/ _ \  |_   _| ____/ ___|_   _|
   / _ \| | | | | || | | |   | | |  _| \___ \ | |  
  / ___ \ |_| | | || |_| |   | | | |___ ___) || |  
 /_/   \_\___/  |_| \___/    |_| |_____|____/ |_|  
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"

      Starting      ...     ...     ...""")
    allure_path = os.path.join(BASE_DIR, 'allure', 'bin', 'allure')
    now_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    allure_data_dir = os.path.join(BASE_DIR, 'report', 'data', now_time)
    allure_report_dir = os.path.join(BASE_DIR, 'report', 'html', now_time)
    test_results = os.path.join(BASE_DIR, 'report', 'video', now_time)
    pytest.main(args=['test_case/UI', f'--output={test_results}', f'--alluredir={allure_data_dir}'] )
    # os.system(f'{allure_path} generate {allure_data_dir} -o  {allure_report_dir} -c')
    # os.system(f'{allure_path} open {allure_report_dir}')


if __name__ == '__main__':
    start_autotest()
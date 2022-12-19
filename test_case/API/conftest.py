#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         :conftest.py
Description      :
Time             :2021/12/18 09:37:43
Author           :AllenLuo
Version          :1.0
'''

import pytest
from tools.read_file import ReadFile
import time
from _pytest import terminal
from loguru import logger 
from tools.sql_operate import Sqloperate
from datetime import datetime

now_time = datetime.now().strftime('%Y%m%d-%H%M%S')

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果并写入数据库'''
    logger.info("===============pytest_terminal_summary===================")
    logger.info(terminalreporter.stats)
    total = terminalreporter._numcollected
    logger.info(f"total:{total}")
    passed = len(terminalreporter.stats.get('passed', []))
    logger.info(f"passed:{passed}")
    failed = len(terminalreporter.stats.get('failed', []))
    logger.info(f"failed:{failed}")
    error = len(terminalreporter.stats.get('error', []))
    logger.info(f"error:{error}")
    skipped = len(terminalreporter.stats.get('skipped', []))
    logger.info(f"skipped:{skipped}")
    passed_rate = '{:.2f}'.format(passed*100/total)
    logger.info(f'passed rate:{passed_rate}%')
    duration = '{:.3f}'.format(time.time() - terminalreporter._sessionstarttime)
    logger.info(f'total times:{duration}seconds')
    report_path = f'/report/html/{now_time}'
    Sql = f'INSERT INTO book_demo.Api_test_result set total={total}, passed={passed},failed={failed},error={error},skipped={skipped},passed_rate="{passed_rate}%",report_path="{report_path}",create_time=now(),update_time=now();'
    # mysql=ReadFile.read_config('$.test_case_database')
    # Sqloperate(mysql=mysql).execute_sql(Sql)


@pytest.fixture(params=ReadFile.get_database_testcase()) # get case from database
def cases(request):
    """ 参数化接口测试用例 """
    return request.param

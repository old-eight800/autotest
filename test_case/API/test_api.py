#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         :test_api.py
Description      :
Time             :2021/12/18 09:37:33
Author           :AllenLuo
Version          :1.0
'''

from .conftest import pytest

from api import client
from tools.data_process import DataProcess


def test_main(cases): 
    # send request and get the respone, API expect and sql expect
    response, api_expect, sql_result, sql_expect = client.action(cases)
    # assert the results
    DataProcess.assert_result(response, api_expect, sql_result, sql_expect)

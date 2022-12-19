#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : test_my_application.py
Description      : 
Time             : 2022/12/10 11:09:08
Author           : AllenLuo
Version          : 1.0
'''

import re
from page.home import *
import os
import yaml
from tools import BASE_DIR
from loguru import logger
from tools import allure_title, allure_step, allure_step_no

test_case_path = os.path.join(BASE_DIR,"test_case","UI","test_case.yaml")
with open(test_case_path, "r", encoding="utf-8") as file:
    case_dict = yaml.load(file.read(), Loader=yaml.FullLoader)

def test_case(uicases, page: Page):
    caseno = list(uicases.keys())[0]
    descrption = dict(list(uicases.values())[0])["descrption"]
    test_step = list(uicases.values())[0]["test_step"]
    expect_result = dict(list(uicases.values())[0])["expect_result"]
    allure_title(caseno)
    allure_step_no(f'descrption:{descrption}')
    allure_step_no(f'test_step:{str(test_step)}')
    i =1
    for k, v in test_step.items():
        if k == "open":
            page_open(page, url=v)
        elif k == f"click{i}":
            page_element_click(page=page, selector=v)
        elif k == f"fill{i}":
            page_element_input_fill(page=page, selector=v["selector"], value=v["value"])
        elif k == f"swipe{i}":
            page_swipe(v["x"], v["y"])
        elif k == "sleep":
            page.wait_for_timeout(v)
        page.wait_for_timeout(1000)
    allure_step_no(f'expect_result:{str(expect_result)}')
    assert expect_result["value"] == page.query_selector(selector=expect_result["selector"]).inner_text()

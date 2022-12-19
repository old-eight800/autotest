#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         :__init__.py
Description      :
Time             :2021/12/18 09:36:43
Author           : AllenLuo
Version          :1.0
'''

import re
from string import Template
from typing import Any
import json
import allure

from jsonpath import jsonpath
from loguru import logger
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

def exec_func(func: str) -> str:
    """ the execution function 
    :params  call the function with str type
    : return str result
    """
    loc = locals() # return the value currently 
    exec(f"result = {func}") 
    return str(loc['result'])


def extractor(obj: dict, expr: str = '.') -> Any:
    """
    :param obj : dict type object
    :param expr: expression, for .  means the whole vaules
    """
    try:
        if not jsonpath(obj, expr):
            # if the object is not json format then do this method
            split_expr = expr.rsplit('.', maxsplit=1)
            expr_sec = split_expr[-2]
            expr_first = split_expr[-1]
            result_sec = jsonpath(obj, expr_sec)[0]
            result = json.loads(result_sec)[expr_first]
        else:
            result = jsonpath(obj, expr)[0]
    except Exception as e:
        logger.error(f'{expr} - cannot extract the dict for {e}')
        result = expr
    return result


def rep_expr(content: str, data: dict) -> str:
    """
    :param content: the origin character string
    :param data: 
    return content： the character string that be replaced 
    """
    logger.info(f'content-{content}')
    content = Template(content).safe_substitute(data)
    for func in re.findall('\\${(.*?)}', content):
        try:
            logger.info(f"exec_func(func)-{exec_func(func)}")
            content = content.replace("${%s}" % func, exec_func(func))
        except Exception as e:
            logger.error(f'rep_expr-{e}')
    return content


def convert_json(dict_str: str) -> dict:
    """
    :param dict_str: dict-like character string 
    return json type
    """
    try:
        if 'None' in dict_str:
            dict_str = dict_str.replace('None', 'null')
        elif 'True' in dict_str:
            dict_str = dict_str.replace('True', 'true')
        elif 'False' in dict_str:
            dict_str = dict_str.replace('False', 'false')
        dict_str = json.loads(dict_str)
    except Exception as e:
        if 'null' in dict_str:
            dict_str = dict_str.replace('null', 'None')
        elif 'true' in dict_str:
            dict_str = dict_str.replace('true', 'True')
        elif 'false' in dict_str:
            dict_str = dict_str.replace('false', 'False')
        dict_str = eval(dict_str)
        logger.error(f'dict_str-{dict_str}')
        logger.error(e)
    return dict_str


def allure_title(title: str) -> None:
    """the title show in allure report"""
    allure.dynamic.title(title)
    logger.info(f'title:{title}')

def allure_step(step: str, var: str) -> None:
    """
    :param step: test steps
    :param var: test attachment
    """
    with allure.step(step):
        allure.attach(
            json.dumps(
                var,
                ensure_ascii=False,
                indent=4),
            step,
            allure.attachment_type.JSON)
    logger.info(f'step:{step}')


def allure_step_no(step: str):
    """
    :param step: test steps
    :return:
    """
    with allure.step(step):
        logger.info(f'step:{step}')

#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : home.py
Description      : 
Time             : 2022/12/10 14:42:01
Author           : AllenLuo
Version          : 1.0
'''

from playwright.sync_api import Page, expect
import allure
from loguru import logger


def page_element_click(page: Page, selector,index=0):
    """ 登录页面点击事件 
        selector: 选择器
        index 匹配的选择器, 默认匹配第1个
    """
    with allure.step(f'点击了元素-{selector}'):
        logger.info(f'点击了元素-{selector}')
    page.locator(selector=selector).nth(index).click()

def page_element_input_fill(page: Page, selector, value):
    """ 页面input框文本填充 """
    with allure.step(f'元素-{selector},填充文本-{value}'):
        logger.info(f'元素-{selector},填充文本-{value}')
    page.fill(selector=selector, value=value)

def page_element_input_fill2(page: Page, placeholder_text, value, index=1):
    """ 页面input框文本填充 """
    with allure.step(f'{placeholder_text}-输入框,填充文本-{value}'):
        logger.info(f'{placeholder_text}-输入框,填充文本-{value}')
    page.get_by_placeholder(text=placeholder_text).nth(index).fill(value=value)

def page_swipe(page: Page, x, y):
    """ 页面滑动方法封装 """
    with allure.step(f'滑动元素,坐标-{x, y}'):
        logger.info(f'滑动元素,坐标-{x, y}')
    page.mouse.wheel(delta_x=x, delta_y=y)

def page_open(page: Page, url):
    """ 打开页面方法封装 """
    with allure.step(f'打开-{url}'):
        logger.info(f'打开-{url}')
    page.goto(url=url)

        

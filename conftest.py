#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : conftest.py
Description      : 
Time             : 2023/02/25 11:13:34
Author           : AllenLuo
Version          : 1.0
'''

def pytest_collection_modifyitems(session, items):
    # sort排序，根据用例名称item.name的ASCII码排序
    items.sort(key=lambda x: x.name)
#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         :read_file.py
Description      :
Time             :2021/12/18 09:37:22
Author           : AllenLuo
Version          :1.0
'''

import yaml
import xlrd
from tools import extractor
import pymysql
from pathlib import Path
from tools import logger


class ReadFile:
    config_dict = None
    config_path = f"{str(Path(__file__).parent.parent)}/config/config.yaml"

    @classmethod
    def get_config_dict(cls) -> dict:
        """
        return cls.config_dict
        """
        if cls.config_dict is None:
            with open(cls.config_path, "r", encoding="utf-8") as file:
                cls.config_dict = yaml.load(
                    file.read(), Loader=yaml.FullLoader)
        return cls.config_dict

    @classmethod
    def read_config(cls, expr: str = ".") -> dict:
        """get the config from config.yaml
        :param expr: using the jsonpath to get the config object
        return
        """
        return extractor(cls.get_config_dict(), expr)

    @classmethod
    def read_testcase(cls):
        """
        get the excel case
        :return generator
        """
        book = xlrd.open_workbook(cls.read_config("$.file_path.test_case"))
        # get the first sheet
        table = book.sheet_by_index(0)
        for norw in range(1, table.nrows):
            # Determine whether a case needs to be executed
            # IF the IsExecute  is N it will ot be executed
            if table.cell_value(norw, 5) != "N":
                value = table.row_values(norw)
                value.pop(5)
                yield value
                logger.info(f'value-{value}')

    @classmethod
    def get_database_testcase(cls):
        """
        get API test case from database

        """
        conn = pymysql.connect(
            host=cls.read_config("$.test_case_database.host"),
            port=cls.read_config("$.test_case_database.port"),
            user=cls.read_config("$.test_case_database.user"),
            password=cls.read_config("$.test_case_database.password"),
            db=cls.read_config("$.test_case_database.db_name"),
            cursorclass=pymysql.cursors.DictCursor
        )
        query_sql = 'select CaseNo, Summary, Domain, RquestHeader, InterfacePath, IsExecute, Encode, MethodType, ParamsType, UploadFile, Params, `Sql` , extract, APIExpectResult, SqlExpectResult from Api_test_detail;'
        try:
            cursor = conn.cursor()  
            cursor.execute(query_sql)  # 游标执行sql语句
            results = cursor.fetchall()
            for row in results:
                lst = []
                if row['IsExecute'] == 'Y':
                    lst.append(row['CaseNo'] if row['CaseNo'] else '')
                    lst.append(row['Summary'] if row['Summary'] else '')
                    lst.append(row['Domain'] if row['Domain'] else '')
                    lst.append(row['RquestHeader']
                               if row['RquestHeader'] else '')
                    lst.append(row['InterfacePath']
                               if row['InterfacePath'] else '')
                    lst.append(row['Encode'] if row['Encode'] else '')
                    lst.append(row['MethodType'] if row['MethodType'] else '')
                    lst.append(row['ParamsType'] if row['ParamsType'] else '')
                    lst.append(row['UploadFile'] if row['UploadFile'] else '')
                    lst.append(row['Params'] if row['Params'] else '')
                    lst.append(row['Sql'] if row['Sql'] else '')
                    lst.append(row['extract'] if row['extract'] else '')
                    lst.append(row['APIExpectResult']
                               if row['APIExpectResult'] else '')
                    lst.append(row['SqlExpectResult']
                               if row['SqlExpectResult'] else '')
                    yield lst
        finally:
            cursor.close()
            conn.close()

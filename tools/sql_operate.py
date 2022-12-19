#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : sql_operate.py
Description      : the sql operation file
Time             : 2022/01/02 12:55:52
Author           : AllenLuo
Version          : 1.0
'''

import json
from datetime import datetime
from typing import Union
import pymysql
from tools.read_file import ReadFile


class Sqloperate:
    mysql = ReadFile.read_config('$.database')

    def __init__(self):
        """
        initialize the mysql connection
        """
        self.connection = pymysql.connect(
            host=self.mysql['host'],
            port=self.mysql['port'],
            user=self.mysql['user'],
            password=self.mysql['password'],
            db=self.mysql['db_name'],
            charset=self.mysql.get('charset', 'utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute_sql(self, sql: str) -> Union[dict, None]:
        """
        execute the sql
        there will be only one result returns, 
        so you should write the sql which can fetch one result
        For we have compare the result, and cannot return too many results to us.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()  
            self.connection.commit()
            self.connection.close()
            return self.verify(result)

    def verify(self, result: dict) -> Union[dict, None]:
        """serializers the results """
        try:
            json.dumps(result)
        except TypeError:   # TypeError: Object of type datetime is not JSON serializable
            for k, v in result.items():
                if isinstance(v, datetime):
                    result[k] = str(v)
        return result
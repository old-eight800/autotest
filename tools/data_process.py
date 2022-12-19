#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         :data_process.py
Description      :
Time             :2021/12/18 09:37:11
Author           : AllenLuo
Version          :1.0
'''
from tools import logger, extractor, convert_json, rep_expr, allure_step, allure_step_no
from tools.read_file import ReadFile

class DataProcess:
    # a pool to save paramters 
    extra_pool = {}
    header = ReadFile.read_config('$.request_headers')

    @classmethod
    def handle_path(cls, domain: str, path_str: str) -> str:
        """
        :param path_str: 
        :param domain: 
        
        return  the extact string
        """
        url = rep_expr(domain, cls.extra_pool) + rep_expr(path_str, cls.extra_pool)
        allure_step_no(f'request url: {url}')
        return url

    @classmethod
    def handle_header(cls, header_str: str) -> dict:
        """
        :header_str: 
        return header: 
        """
        if header_str == '':
            header_str = '{}'
        cls.header.update(cls.handle_data(header_str))
        allure_step('request header', cls.header)
        return cls.header

    @classmethod
    def handler_files(cls, file_obj: str) -> object:
        """
        :param file_obj: upload file 
        
        """
        if file_obj != '':
            for k, v in convert_json(file_obj).items():
                # Multiple files upload
                if isinstance(v, list):
                    files = []
                    for path in v:
                        files.append((k, (open(path, 'rb'))))
                else:
                    # Single files upload
                    files = {k: open(v, 'rb')}
            allure_step('upload file', file_obj)
            return files

    @classmethod
    def handle_data(cls, variable: str) -> dict:
        """
        :param variable: 
        return json-like , dict-like data
        """
        if variable != '':
            logger.info(f'extra_pool-{cls.extra_pool}')
            data = rep_expr(variable, cls.extra_pool)
            variable = convert_json(data)
            logger.info(f'variable-{variable}')
            return variable

    @classmethod
    def handle_extra(cls, extra_str: str, response: dict):
        """
        :param extra_str: the extract fields in excel,it must be {"paramters": "jsonpath"} format
        :param response: 
        """
        if extra_str != '':
            extra_dict = convert_json(extra_str)
            for k, v in extra_dict.items():
                cls.extra_pool[k] = extractor(response, v)
                logger.info(f'add the extract to dict ,key: {k}, value: {v}')

    @classmethod
    def assert_result(cls, response: dict, api_expect_str: str, sql_result: dict, sql_expect_str: str):
        """ 
        :param response: the acctual result
        :param expect_str: the expect result，get it form excel
        return None
        """
        allure_step("the available extract in the paramters pool currently", cls.extra_pool)
        if sql_expect_str:
            sql_expect = rep_expr(sql_expect_str, cls.extra_pool)
            sql_expect_dict = convert_json(sql_expect)
            sql_index = 0
            for sql_k, sql_v in sql_expect_dict.items():
                sql_result_actual = extractor(sql_result, sql_k)
                sql_index +=1
                logger.info(
                f'the {sql_index}th sql assert,sql acctual result:{sql_result} | sql expect result:{sql_expect_dict} the assert result:{sql_result_actual == sql_v}')
                logger.info(
                f'第{sql_index}个断言,sql实际结果:{sql_result} | sql预期结果:{sql_expect_dict} sql断言结果 {sql_result_actual == sql_v}\n')
                allure_step(f'the {sql_index}th sql assert', f'sql acctual result:{sql_result} contains sql expect result:{sql_expect_dict}')
                try:
                    assert sql_result_actual == sql_v
                except AssertionError:
                    raise AssertionError(
                        f'the {sql_index}th sql assert failed -|- sql acctual result:{sql_result} || sql expect result: {sql_expect_dict}\n',
                        f'第{sql_index}个sql断言失败 -|- sql实际结果:{sql_result} || sql预期结果: {sql_expect_dict}')

        api_expect = rep_expr(api_expect_str, cls.extra_pool)
        api_expect_dict = convert_json(api_expect)
        index = 0
        for k, v in api_expect_dict.items():
            actual = extractor(response, k)
            index += 1
            logger.info(
                f"the {index}th api assert, acctual result:{actual} | expect result:{v} the assert result:{actual == v}\n",
                f"第{index}个api接口断言,实际结果:{actual} | 预期结果:{v} 断言结果 {actual == v}")
            allure_step(f'the {index}th api assert', f'acctual result:{actual} = expect result:{v}')
            try:
                assert actual == v
            except AssertionError:
                raise AssertionError(
                    f'the {index}th api assert failed -|- acctual result:{actual} || expect result: {v}\n',
                    f'第{index}个api接口断言失败 -|- 实际结果:{actual} || 预期结果: {v}')

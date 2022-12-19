#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         :client.py
Description      :
Time             :2021/12/18 09:38:07
Author           :AllenLuo
Version          :1.0
'''

from typing import Any
from requests import Session
from tools import allure_step, allure_title, logger, allure_step_no
from tools.data_process import DataProcess
from tools.sql_operate import Sqloperate
from tools.encode import *
from tools.read_file import ReadFile
from tools.generate_data import *

class Transmission:
    PARAMS: str = "params"
    DATA: str = "data"
    JSON: str = "json"


class Client(Session):

    def action(self, case: list, Domain: str = "Domain") -> Any:
        """Parsing the excel data and change it to data that can be send
        :param case: unpack the excel data
        :param Domain: access domain for sending a request
        return: response ExpectResult
        """
        (   
            CaseNo,
            Summary,
            Domain,
            RquestHeader,
            InterfacePath,
            Encode,
            MethodType,
            ParamsType,
            UploadFile,
            Params,
            Sql,
            extract,
            APIExpectResult,
            SqlExpectResult
        ) = case
        logger.debug(
            f"用例进行处理前数据: \n接口路径: {InterfacePath} \n是否需要加密：{Encode} \n请求参数: {Params} \n要执行的sql：{Sql} \n提取参数: {extract} \n接口预期结果: {APIExpectResult} \nSql预期结果: {SqlExpectResult} \n  "
        )
        # values_config = ReadFile.read_config('$.value')
        for k, v in config_dict.items():
            if k in Params:
                Params = Params.replace(f'{k}', v)
        # allure report title
        allure_title(Summary)
        url = DataProcess.handle_path(Domain, InterfacePath)
        header = DataProcess.handle_header(RquestHeader)
        Params = DataProcess.handle_data(Params)
        allure_step("request paramters", Params)
        allure_step("execute sql", Sql)
        if UploadFile:
            allure_step("upload file is", UploadFile)
            print(f"UploadFile-{UploadFile}")
        file = DataProcess.handler_files(UploadFile)
        # send the request
        response = self._request(url, Encode, InterfacePath, MethodType, ParamsType, header, Params, file)
        # get the rely on paramaters
        DataProcess.handle_extra(extract, response)
        if Sql: # if sql exists, then execute the sql
            mysql=ReadFile.read_config('$.database')
            sql_result = Sqloperate(mysql=mysql).execute_sql(Sql)
            logger.info(f'sql execute result-{sql_result}')
            allure_step("sql execute result", sql_result)
        else:
            sql_result = ''
        return response, APIExpectResult, sql_result, SqlExpectResult

    def _request(
        self, url, Encode, InterfacePath, method, ParamsType, header=None, Params=None, UploadFile=None
    ) -> dict:
        """
        :param method: MethodType the request type
        :param url: request url
        :param Encode: if need to encode the interface
        :param api_path: the api path like /IM/calculateIRR
        :param ParamsType: the params type
        :param Params: the request params
        :param UploadFile: the file upload to server
        :param header: 
        :return: respones
        """

        if ParamsType == Transmission.PARAMS:
            extra_args = {Transmission.PARAMS: Params}
        elif ParamsType == Transmission.DATA:
            extra_args = {Transmission.DATA: Params}
        elif ParamsType == Transmission.JSON:
            extra_args = {Transmission.JSON: Params}
        else:
            raise ValueError("the key word must be one of params, json, data")
        if Encode =='Y':
            values_config = ReadFile.read_config('$.value')
            encode_url = "http://172.27.77.86:8443"
            ciphertext_data_request = encode_request(encode_url, plaintext_data=Params, ChannelNo=values_config['channelNo'])
            ciphertext_data_respone = encode_respone(url, ciphertext_data=ciphertext_data_request)
            logger.info(f"ciphertext_data_respone-{ciphertext_data_respone}")
            response =decode_response(url=encode_url, data=ciphertext_data_respone)
            logger.info(
                f"\n最终请求地址:{url}\n请求方法:{method}\n请求头:{header}\n请求参数:{Params}\n上传文件:{UploadFile}\n响应数据:{response}"
            )
            # allure_step_no(f"respone elapsed time(s): {res.elapsed.total_seconds()}")
        else:
            res = self.request(
                method=method, url=url, files=UploadFile, headers=header, **extra_args
            )
            response = res.json()
            logger.info(
                f"\n最终请求地址:{res.url}\n请求方法:{method}\n请求头:{header}\n请求参数:{Params}\n上传文件:{UploadFile}\n响应数据:{response}"
            )
            allure_step_no(f"respone elapsed time(s): {res.elapsed.total_seconds()}")
        allure_step("API respone result", response)
        return response


client = Client()

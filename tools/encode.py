# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :   encode.py
@Time    :   2022/01/15 19:52:58
@Author  :   AllenLuo
@Version :   1.0
@Contact :   username@163.com
@Desc    :   None
"""

import string
import requests
import json
from tools import logger
def encode_request(url, plaintext_data, ChannelNo="CUP CAR LOAN_YIXIN") -> json:
  """
  Description: 入参加密方法
  ---------
  Arguments: url: 入参加密链接
             plaintext_data: 明文入参
  ---------
  Returns:
  -------
  """
  try: 
    raw_url = f"{url}/IM/encode/request/?apiId=100008&transNo=159463662161357829085&reqTime=20200713063705&reqChannelNo={ChannelNo}&rspChannelNo={ChannelNo}"
    request_payload = json.dumps(plaintext_data)
    logger.debug(f"请求的明文入参:{request_payload}")
    req_response = requests.request("POST", raw_url, data=request_payload)
    return req_response.json()
  except BaseException as e:
    logger.error(f'encode_request error-{e}')

def decode_request(url, ciphertext_data) -> string:
  """
  
  Description: 入参解密方法
  ---------
  
  Arguments: url: 入参解密链接 
             ciphertext_data: 密文入参
  ---------
  
  
  Returns:
  -------
  
  """
  url = f"{url}/IM/decode/request"
  decode_request_payload = json.dumps(ciphertext_data) # 转化为json传输
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=decode_request_payload)
  logger.debug(f"入参解密后：{response.text}")
  return response.text
  
def encode_respone(url, ciphertext_data) -> string:
  """
  
  Description: 出参加密 
  ---------
  
  Arguments:url：  需要加密的接口链接
            api_path: 接口路径 如 /IM/calculateIRR
            ciphertext_data:  加密入参
  ---------

  Returns: 返回json格式响应数据
  -------
  
  """

  headers = {
    'Content-Type': 'application/json'
  }
  encode_response = requests.request("POST", url=url, headers=headers, data=json.dumps(ciphertext_data))
  logger.debug(f"出参加密:{encode_response.text}")
  return encode_response.text


def decode_response(url, data) -> string:
  try:
    decode_response_url = url + "/IM/decode/response"
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url=decode_response_url, headers=headers, data=data)
    logger.debug(f"出参解密后：{response.text}")
    return json.loads(response.text)
  except BaseException as e:
    logger.error(f'decode_response error-{e}')

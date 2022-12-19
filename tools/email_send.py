#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : email_send.py
Description      : 
Time             : 2022/02/22 16:55:53
Author           : AllenLuo
Version          : 1.0
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tools.read_file import ReadFile
import time
from tools import logger

def email_send(subject, email_content):
    """
    
    Description: 邮件发送方法
    ---------
    Arguments:  subject 邮件主题， email_content 邮件正文
    --------- 
    Returns:  
    -------
    
    """
    emai_config = ReadFile.read_config('$.emai')
    sender = emai_config['sender']
    receivers = emai_config['receivers']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(email_content, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')   # 发送者
    message['Subject'] = Header(subject, 'utf-8')
        # 接收者
    try:
        smtpObj = smtplib.SMTP(emai_config['mail_host'])
        for receiver in receivers:
            message['To'] =  Header(receiver, 'utf-8')
        smtpObj.sendmail(sender, receivers, message.as_string())
        return logger.info(f'邮件发送成功,接收者{receivers}')
    except smtplib.SMTPException as e:
        return logger.error(f'邮件发送失败-{e}')

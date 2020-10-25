#!/usr/bin/python
# -*- coding:utf8 -*-
import os

#邮件发送相关
BASE_PATH = os.path.dirname(
   os.path.dirname(os.path.abspath(__file__))  #便于将日志重放logs文件中，这里取到该父文件夹的地址
)
MAIL_HOST='smtp.163.com'   #host
MAIL_USER='lisha_chen123@163.com'   #用户名
MAIL_PASSWRD = 'CLS123456'    #授权码
TO = [
   'lisha.chen@mshare.cn',       #发送
]
LEVEL = 'debug' #日志级别

LOG_PATH = os.path.join(BASE_PATH,'logs') #存放日志的路径，经过拼接
CASE_PATH = os.path.join(BASE_PATH,'cases') #存放日志的路径，经过拼接
RESULT_PATH = os.path.join(BASE_PATH,'result') #存放结果的路径，经过拼接
LOG_NAME = 'atp.log' #日志的文件名，定义在这比较好修改

#登录相关
# LOGIN_URL = "https://www.shixiseng.com/user/login" #存放登录请求地址
# LOGIN_USER = "15802380900" #存放登录用户名
# LOGIN_PASSWORD = "45X35X25X15X05X94" #存放登录密码

#测试环境-登录
LOGIN_URL = "http://sit1-sxs-web.mshare.cn/user/login" #存放登录请求地址
LOGIN_USER = "18782950040" #存放登录用户名
LOGIN_PASSWORD = "45X35X25X15X05X94" #存放登录密码
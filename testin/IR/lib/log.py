#!/usr/bin/python
# -*- coding:utf8 -*-
import logging,os
from logging import handlers
from IR.conf import setting
class MyLogger():
   def __init__(self,file_name,level='info',backCount=5,when='D'):
      logger = logging.getLogger()  # 先实例化一个logger对象
      logger.setLevel(self.get_level(level))  # 设置日志的级别
      cl = logging.StreamHandler()  # 将日志输出到控制台
      bl = handlers.TimedRotatingFileHandler(filename=file_name, when=when,
                                             interval=1, backupCount=backCount, encoding='utf-8') #日志输入到文件
      fmt = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
      cl.setFormatter(fmt)  # 设置控制台输出的日志格式
      bl.setFormatter(fmt)  # 设置文件里面写入的日志格式
      logger.addHandler(cl)
      logger.addHandler(bl)
      self.logger = logger

   def get_level(self,str):
      level = {
         'debug':logging.DEBUG,
         'info':logging.INFO,
         'warn':logging.WARNING,
         'error':logging.ERROR
      }
      str = str.lower()
      return level.get(str)


path = os.path.join(setting.LOG_PATH,setting.LOG_NAME) #拼好日志的绝对路径
atp_log = MyLogger(path,setting.LEVEL).logger
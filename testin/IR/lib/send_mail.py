#!/usr/bin/python
# -*- coding:utf8 -*-
import yagmail
from IR.conf import setting  #配置文件
from IR.lib.log import atp_log


def sendmail(title,content,attrs=None):
   m = yagmail.SMTP(host=setting.MAIL_HOST,user=setting.MAIL_USER
             ,password=setting.MAIL_PASSWRD
             )                                        #sllm = ture 有些需要  连接数据库
   m.send(to=setting.TO,subject=title,
         contents=content,
         attachments=attrs)                                  #这里可以try要一下
   atp_log.info('发送邮件完成')

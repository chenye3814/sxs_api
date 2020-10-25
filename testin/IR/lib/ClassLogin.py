#!/usr/bin/python
# -*- coding:utf8 -*-
import requests
from IR.lib.log import atp_log
from IR.lib.common import OpCase
import json

op=OpCase()

class ClassLogin():
    def login(self, url, data):  # 获取ookie
        session=requests.session()
        data = op.dataToDict(data)
        try:
            res = session.post(url, data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True)
            #cookies = requests.utils.dict_from_cookiejar(res.cookies) #获取cookies
            cookie=session.cookies

        except Exception as e:
            msg = '【%s】登录接口失败，%s' % (url, e)  # 处理接口未调用成功的信息
            atp_log.error(msg)
        return cookie





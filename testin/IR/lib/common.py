# -*- coding:utf8 -*-

import xlrd
from xlutils import copy
from IR.lib.log import atp_log
import requests
from jsonschema import validate
import json
from IR.lib.Custom_param import Custom_p

class OpCase(object):

    def get_case(self, file_path):

        cases = []  # 存放所有的case
        if file_path.endswith('.xls') or file_path.endswith('.xlsx'):  # 判断给出的文件是否是excel文件
            try:
                book = xlrd.open_workbook(file_path)  # 打开文件
                sheet = book.sheet_by_index(0)  # 获取第一页的内容
                for i in range(1, sheet.nrows):  # 数据从1开始，跳过标题
                    row_data = sheet.row_values(i)  # 获取每行的数据
                    cases.append(row_data[2:10])  # 利用切片取到所使用3-7列的数据并加入list 应该是一个二维数组
                atp_log.info('共读取%s条用例' % (len(cases)))  # 取list的长度为用例的个数。
                self.file_path = file_path  ##便于写excel时直接使用路径。
            except Exception as e:
                atp_log.error('【%s】用例获取失败，错误信息：%s' % (file_path, e))  # 处理打不开文件 比如文件损坏
        else:
            atp_log.error('用例文件不合法的，%s' % file_path)  # 不是excel文件日志报错
        return cases

    def my_request(self, sys_way, url, method, data, is_login, cookie):  # 用来调接口
        method = method.upper()  # 防止接口的大小写问题。都转化为大写
        if '{' in data and data[0] == '{':
            pass
        else:
            data = self.dataToDict(data)  # 将数据转化为字典
            data = self.change_custom_param(data)   # 替换传参中有函数的参数
            print('data', data)

        if sys_way == "APP":  # 根据项目切换不同的请求头
            headers = {'User-Agent': "sxsiosapp/4.1.0"}
        elif sys_way == "MINA":
            headers = {'sxsminiprogram': "common_mina"}
        elif sys_way == "CT":
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
            # headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        elif sys_way == "CTaj":
            headers = {'Content-Type': 'application/json'}
        else:
            headers = None

        try:
            if is_login == 't':
                if method == 'POST':
                    res = requests.post(url, data=data, cookies=cookie,
                                        headers=headers).text  # res正常会返回一个字典，但如果结果110状态码就会报错，.text转化后就不报错，都能获取到值。
                elif method == 'GET':
                    res = requests.get(url, params=data, cookies=cookie, headers=headers).text
                else:
                    atp_log.warning('该请求方式暂不支持。。')
                    res = '该请求方式暂不支持。。'  # 没有res会报错  否者就没有res
            else:
                if method == 'POST':
                    res = requests.post(url, data,
                                        headers=headers).text  # res正常会返回一个字典，但如果结果110状态码就会报错，.text转化后就不报错，都能获取到值。
                elif method == 'GET':
                    res = requests.get(url, params=data, headers=headers).text
                else:
                    atp_log.warning('该请求方式暂不支持。。')
                    res = '该请求方式暂不支持。。'  # 没有res会报错  否者就没有res

        except Exception as e:
            msg = '【%s】接口调用失败，%s' % (url, e)  # 处理接口未调用成功的信息
            atp_log.error(msg)
            res = msg
        # return_res = res.encode().decode('unicode_escape')
        return res

    def check_res(self, res, check):  # 校验结果 实际结果和预期结果
        res = res.replace('": "', '=').replace('": ', '=')  # 替换符号为=号，两次替换
        for c in check.split(','):  # 根据，去才分预期和结果进行对比
            if c not in res:  # 判断该字符串是否包含C的整体
                atp_log.info('结果校验失败，预期结果：【%s】，实际结果不包含预期结果【%s】' % (c, res))
                return '失败'
        return '通过'

    def check_json(self, data, schema):
        r = data.replace("null", '""')
        data_json = json.loads(r)
        schema_json = json.loads(schema)
        try:
            result = validate(data_json, schema_json)  # 校验json格式
            if result == None:
                return "通过"
            else:
                return result
        except Exception as e:
            msg = '对比失败，%s' % (e)  # 处理接口未调用成功的信息
            return msg

    def write_excel(self, cases_res, result_path):  # 结果写入excel
        # [ ['dsfd',"通过"] ,['sdfsdf','失败'] ]
        book = xlrd.open_workbook(self.file_path)  # 打开文档
        new_book = copy.copy(book)
        sheet = new_book.get_sheet(0)  # 获取sheet页
        row = 2
        for case_case in cases_res:
            if len(case_case[0]) < 32300:
                sheet.write(row, 10, case_case[0])  # 写第9列
            else:
                sheet.write(row, 10, "结果过大，请单独请求")  # 写第9列
            if len(case_case[1]) < 32300:
                sheet.write(row, 11, case_case[1])  # 写第10列
            else:
                sheet.write(row, 11, "结果过大，请单独请求")  # 写第10列
            row += 1
        new_book.save(result_path.replace('xlsx', 'xls'))  # 结尾必须以xls结尾才能保存

    def dataToDict(self, data):  # 处理参数输入的格式 一般要求a=b之类的简单格式如何转换为可以发送的数据格式。
        # 把数据转成字典
        res = {}
        if data:
            data = data.split(',')
        for d in data:
            # a=   没值时后面为空 不需要处理
            k, v = d.split('=')
            res[k] = v
        return res

    def change_custom_param(self, data_dict):
        """将含有自定义方法的参数执行后的结果赋值到对应的参数上"""
        if isinstance(data_dict, dict):
            for k, v in data_dict.items():
                if 'Custom_p' in v:
                    data_dict[k] = eval(v)
                else:
                    pass
        else:
            pass
        return data_dict


if __name__ == '__main__':
    op = OpCase()
    data = {"code": 100, "msg": [{"uuid": "inn_ouqunkngyibl", "name": "新媒体-yyl",
                                  "info": "\u003cp\u003e\n\t编辑1\n\u003c/p\u003e\n\u003cp\u003e\n\t新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl\u003cspan\u003e新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl新媒体-yyl\u003c/span\u003e\u003cspan\u003e新媒体-yyl\u003c/span\u003e\n\u003c/p\u003e",
                                  "url": "https://sxsimg.xiaoyuanzhao.com/7D/C9/7D7BBA882D02906CA98A776F411666C9.jpg",
                                  "effective_time": 1603971600, "city": "重庆", "day": "5", "minsal": 100, "maxsal": 200,
                                  "company_name": "岳阳楼", "admin_info": "", "company_type": "normal",
                                  "company_status": "normal", "attraction": ["远程实习", "可转正实习", "暑期实习"],
                                  "is_financing": "B轮", "scale": "少于15人", "industry": "互联网/游戏/软件",
                                  "refresh_time": "10-15", "month_num": 3, "company_uuid": "com_tb8wtvv5avga",
                                  "linkedin_num": 0, "tag": "", "status": "normal",
                                  "job_lable": {"is_double_selection": False, "is_hirer": True, "is_hr": False,
                                                "is_ji": False, "is_quick": False}, "salary_desc": "100-200/天",
                                  "intern_type": 0, "uuid_build_time": "2020-08-21 14:43:46", "hope_you": [],
                                  "degree": "不限"}, {"uuid": "inn_ija9vidyhglg", "name": "9.28.测试",
                                                    "info": "\u003cspan\u003e静默AaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1\u003c/span\u003e",
                                                    "url": "https://sxsimg.xiaoyuanzhao.com/7D/C9/7D7BBA882D02906CA98A776F411666C9.jpg",
                                                    "effective_time": 1596758400, "city": "成都", "day": "1",
                                                    "minsal": 100, "maxsal": 100, "company_name": "岳阳楼",
                                                    "admin_info": "", "company_type": "normal",
                                                    "company_status": "normal", "attraction": ["囧哦"],
                                                    "is_financing": "B轮", "scale": "少于15人", "industry": "互联网/游戏/软件",
                                                    "refresh_time": "07-24", "month_num": 4,
                                                    "company_uuid": "com_tb8wtvv5avga", "linkedin_num": 0,
                                                    "tag": "https://sxsimg.xiaoyuanzhao.com/static/img/overdue.png",
                                                    "status": "destroy",
                                                    "job_lable": {"is_double_selection": False, "is_hirer": True,
                                                                  "is_hr": False, "is_ji": False, "is_quick": False},
                                                    "salary_desc": "100/天", "intern_type": 0,
                                                    "uuid_build_time": "2019-06-03 18:00:35", "hope_you": [],
                                                    "degree": "不限"}]}
    schema = {"type": "object", "properties": {"code": {"type": "integer"}, "msg": {"type": "array",
                                                                                    "items": {"type": "object",
                                                                                              "properties": {"uuid": {
                                                                                                  "type": "string"},
                                                                                                  "name": {
                                                                                                      "type": "string"},
                                                                                                  "info": {
                                                                                                      "type": "string"},
                                                                                                  "url": {
                                                                                                      "type": "string"},
                                                                                                  "effective_time": {
                                                                                                      "type": "float"},
                                                                                                  "city": {
                                                                                                      "type": "string"},
                                                                                                  "day": {
                                                                                                      "type": "integer"},
                                                                                                  "minsal": {
                                                                                                      "type": "integer"},
                                                                                                  "maxsal": {
                                                                                                      "type": "integer"},
                                                                                                  "company_name": {
                                                                                                      "type": "string"},
                                                                                                  "admin_info": {
                                                                                                      "type": "string"},
                                                                                                  "company_type": {
                                                                                                      "type": "string"},
                                                                                                  "company_status": {
                                                                                                      "type": "string"},
                                                                                                  "attraction": {
                                                                                                      "type": "array",
                                                                                                      "items": {
                                                                                                          "type": "string"}},
                                                                                                  "is_financing": {
                                                                                                      "type": "string"},
                                                                                                  "scale": {
                                                                                                      "type": "string"},
                                                                                                  "industry": {
                                                                                                      "type": "string"},
                                                                                                  "refresh_time": {
                                                                                                      "type": "string"},
                                                                                                  "month_num": {
                                                                                                      "type": "integer"},
                                                                                                  "company_uuid": {
                                                                                                      "type": "string"},
                                                                                                  "linkedin_num": {
                                                                                                      "type": "integer"},
                                                                                                  "tag": {
                                                                                                      "type": "string"},
                                                                                                  "status": {
                                                                                                      "type": "string"},
                                                                                                  "job_label": {
                                                                                                      "type": "object",
                                                                                                      "properties": {
                                                                                                          "is_quick": {
                                                                                                              "type": "boolean"},
                                                                                                          "is_double_selection": {
                                                                                                              "type": "boolean"},
                                                                                                          "is_ji": {
                                                                                                              "type": "boolean"},
                                                                                                          "is_hr": {
                                                                                                              "type": "boolean"},
                                                                                                          "is_hirer": {
                                                                                                              "type": "boolean"}},
                                                                                                      "required": [
                                                                                                          "is_quick",
                                                                                                          "is_double_selection",
                                                                                                          "is_ji",
                                                                                                          "is_hr",
                                                                                                          "is_hirer"]},
                                                                                                  "salary_desc": {
                                                                                                      "type": "string"},
                                                                                                  "intern_type": {
                                                                                                      "type": "integer"},
                                                                                                  "uuid_build_time": {
                                                                                                      "type": "string"},
                                                                                                  "hope_you": {
                                                                                                      "type": "array",
                                                                                                      "items": {
                                                                                                          "type": "string"}},
                                                                                                  "degree": {
                                                                                                      "type": "string"}},
                                                                                              "required": ["uuid",
                                                                                                           "name",
                                                                                                           "info",
                                                                                                           "url",
                                                                                                           "effective_time",
                                                                                                           "city",
                                                                                                           "day",
                                                                                                           "minsal",
                                                                                                           "maxsal",
                                                                                                           "company_name",
                                                                                                           "admin_info",
                                                                                                           "company_type",
                                                                                                           "company_status",
                                                                                                           "attraction",
                                                                                                           "is_financing",
                                                                                                           "scale",
                                                                                                           "industry",
                                                                                                           "refresh_time",
                                                                                                           "month_num",
                                                                                                           "company_uuid",
                                                                                                           "linkedin_num",
                                                                                                           "tag",
                                                                                                           "status",
                                                                                                           "job_label",
                                                                                                           "salary_desc",
                                                                                                           "intern_type",
                                                                                                           "uuid_build_time",
                                                                                                           "hope_you",
                                                                                                           "degree"]}}},
              "required": ["code", "msg"]}

    data1 = ['CTaj', 'http://istio-test-apigateway.mshare.cn', '/api/account/v3.0/collect/add', 'post',
             "{'type':'intern','uuid':'inn_ouqunkngyibl'}", 't', 'code=100',
             '{"type":"object","properties":{"code":{"type":"integer"}},"required":["code"]}']

    data11 = 'type=intern,uuid=inn_ouqunkngyibl'

    # print(op.dataToDict(data11))
    print(type(op.dataToDict(data11)))

    # data2 = json.dumps(data)
    # # data2 = str(data)
    # print(type(data2))
    # schema2 = json.dumps(schema)
    #
    # # a = {}
    #
    # re=op.check_json(data2,schema2)
    # print(re)

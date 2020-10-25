import requests
import json
from IR.lib.ClassLogin import ClassLogin
import datetime
import time
import hashlib
from IR.lib.Custom_param import Custom_p
#
# a = {'type': 'object', 'properties': {'uuid': {'type': 'string'}, 'name': {'type': 'string'}, 'info': {'type': 'string'}, 'url': {'type': 'string'}, 'effective_time': {'type': 'float'}, 'city': {'type': 'string'}, 'day': {'type': 'integer'}, 'minsal': {'type': 'integer'}, 'maxsal': {'type': 'integer'}, 'company_name': {'type': 'string'}, 'admin_info': {'type': 'string'}, 'company_type': {'type': 'string'}, 'company_status': {'type': 'string'}, 'attraction': {'type': 'array', 'items': {'type': 'string'}}, 'is_financing': {'type': 'string'}, 'scale': {'type': 'string'}, 'industry': {'type': 'string'}, 'refresh_time': {'type': 'string'}, 'month_num': {'type': 'integer'}, 'company_uuid': {'type': 'string'}, 'linkedin_num': {'type': 'integer'}, 'tag': {'type': 'string'}, 'status': {'type': 'string'}, 'job_lable': {'type': 'object', 'properties': {'is_quick': {'type': 'boolean'}, 'is_double_selection': {'type': 'boolean'}, 'is_ji': {'type': 'boolean'}, 'is_hr': {'type': 'boolean'}, 'is_hirer': {'type': 'boolean'}}, 'required': ['is_quick', 'is_double_selection', 'is_ji', 'is_hr', 'is_hirer']}, 'salary_desc': {'type': 'string'}, 'intern_type': {'type': 'integer'}, 'uuid_build_time': {'type': 'string'}, 'hope_you': {'type': 'array', 'items': {'type': 'string'}}, 'degree': {'type': 'string'}}, 'required': ['uuid', 'name', 'info', 'url', 'effective_time', 'city', 'day', 'minsal', 'maxsal', 'company_name', 'admin_info', 'company_type', 'company_status', 'attraction', 'is_financing', 'scale', 'industry', 'refresh_time', 'month_num', 'company_uuid', 'linkedin_num', 'tag', 'status', 'job_lable', 'salary_desc', 'intern_type', 'uuid_build_time', 'hope_you', 'degree']}
# b = {'properties': {'admin_info': {'type': 'string'}, 'attraction': {'items': {'type': 'string'}, 'type': 'array'}, 'city': {'type': 'string'}, 'company_name': {'type': 'string'}, 'company_status': {'type': 'string'}, 'company_type': {'type': 'string'}, 'company_uuid': {'type': 'string'}, 'day': {'type': 'integer'}, 'degree': {'type': 'string'}, 'effective_time': {'type': 'float'}, 'hope_you': {'items': {'type': 'string'}, 'type': 'array'}, 'industry': {'type': 'string'}, 'info': {'type': 'string'}, 'intern_type': {'type': 'integer'}, 'is_financing': {'type': 'string'}, 'job_lable': {'properties': {'is_double_selection': {'type': 'boolean'}, 'is_hirer': {'type': 'boolean'}, 'is_hr': {'type': 'boolean'}, 'is_ji': {'type': 'boolean'}, 'is_quick': {'type': 'boolean'}}, 'required': ['is_quick', 'is_double_selection', 'is_ji', 'is_hr', 'is_hirer'], 'type': 'object'}, 'linkedin_num': {'type': 'integer'}, 'maxsal': {'type': 'integer'}, 'minsal': {'type': 'integer'}, 'month_num': {'type': 'integer'}, 'name': {'type': 'string'}, 'refresh_time': {'type': 'string'}, 'salary_desc': {'type': 'string'}, 'scale': {'type': 'string'}, 'status': {'type': 'string'}, 'tag': {'type': 'string'}, 'url': {'type': 'string'}, 'uuid': {'type': 'string'}, 'uuid_build_time': {'type': 'string'}}, 'required': ['uuid', 'name', 'info', 'url', 'effective_time', 'city', 'day', 'minsal', 'maxsal', 'company_name', 'admin_info', 'company_type', 'company_status', 'attraction', 'is_financing', 'scale', 'industry', 'refresh_time', 'month_num', 'company_uuid', 'linkedin_num', 'tag', 'status', 'job_lable', 'salary_desc', 'intern_type', 'uuid_build_time', 'hope_you', 'degree'], 'type': 'object'}
#
# # print(a == b)
# #
# # aa = '123'
# # bb = 'aaa'
# # dd = ["bbb",'ff']
# #
# # cc = ['kaishi']
# # cc.append(dd)
# # # cc.extend(dd)
# #
# # ee = dd.pop()
# #
# # print(cc)
# #
# # print(dd)
# #
# # print(ee)
#
# # a1=19.2
# # print(type(a1))
#
# case = ['CTaj', 'http://istio-test-apigateway.mshare.cn', '/api/account/v3.0/collect/add', 'post', "{'type':'intern','uuid':'inn_ouqunkngyibl'}", 't']
# # print(type(case[4]))
# # print(case[4])
#
#
#
#
# # d = case[4].replace("\'", '\"')
# # d = json.loads(d)
# # e = eval(d)
# # print('---')
# # print(type(d))
# # if type(d) == dict:
# #     print('这是type(d) %s' % type(d))
# #     d = json.dumps(d)
# #     print(111,type(d))
# #     print(case)
# #
# # a = eval('1234')
# # print(type(a))
#
#
header1 = {'Content-Type': 'application/json'}
header2 = {'Content-Type': 'application/x-www-form-urlencoded'}
lg = ClassLogin()
cookie2 = lg.login(url='http://istio-test-apigateway.mshare.cn/api/account/v2.0/login', data='password=45X35X25X15X05X94,scookie=1,sys=ios,username=18782950041')
#
# cookie1 = 'SXS_XSESSION_ID=2|1:0|10:1602992826|15:SXS_XSESSION_ID|48:ZjZjYjExYjQtMzQ0ZS00NjkyLTk4N2UtNGI2MDYxMjY5Yzkz|aa753d4ff24c04072fff5b3fe8e88774a3710a33bd0c9b8f73ad6e6fef3e6322; SXS_XSESSION_ID_EXP=2|1:0|10:1602992826|19:SXS_XSESSION_ID_EXP|16:MTYwNTU4NDgyNg==|c98627d8d2bdd4c46d6ac9971aa6a0f6bdf45d603acc6fbed6350364226117d4; affefdgx=usr_fa8zyjexofxl; sxs_usr=2|1:0|10:1602992826|7:sxs_usr|24:dXNyX2ZhOHp5amV4b2Z4bA==|94c940a3f0e67ed1cbf30c44218994c50a536f305f7585f5760febf873d85d52; xyz_usr=2|1:0|10:1602992826|7:xyz_usr|48:ZWQ4YzkxNmMtMGNhMy00Nzk5LTk2MTYtNDU2ZjY5MDcxYTgz|85f340b44b99c48a6e1be74b6785ee68e679fcdb5bcc7273e7560e7fee4425c5'
# url1 = 'http://istio-test-apigateway.mshare.cn/api/account/v2.0/collect/cancle'
#
# data1 = '{"type": "xz_intern", "uuid": "inn_7myy8fxllgqw"}'
#
# #批量删除
# url2 = 'http://istio-test-apigateway.mshare.cn/api/account/v3.0/collect/batch/cancle'
#
# #data2='{ "uuid":"[\"inn_7myy8fxllgqw\",\"inn_ouqunkngyibl\"]"}'
# data2='{ "uuid":"[\"inn_7myy8fxllgqw\"]"}'
#
# #上传文件
# url3="http://istio-test-apigateway.mshare.cn/api/account/v3.0/upload"
# data3={"image":("233.jpg",open("233.jpg","rb"),"image/jpeg")}
# print(data1[0])
# # data2 = json.dumps(data1)
# header1 = {'Content-Type': 'application/json'}
#
# #req = requests.post(url=url2,data=data2,cookies=cookie2,headers=header1)
# #上传文件
# req = requests.post(url=url3,files=data3,cookies=cookie2)
#
# print('--------------')
# print(req.text)

# c1={"city":"成都".encode('utf-8')}
#
# print(c1)

# 批量取消收藏-已解决
# url_c1 = 'http://istio-test-apigateway.mshare.cn/api/account/v3.0/collect/batch/cancle'
# data_c1 = '{"uuid": "[\"inn_7myy8fxllgqw\",\"inn_ouqunkngyibl\"]"}'
# headers_c1 = {'Content-Type': 'application/json'}


# 更新城市缓存-已解决
# url_c2 = 'http://istio-test-apigateway.mshare.cn/api/account/v3.0/cityhistory'
# data_c2 = '{"city":"成都"}'
# headers_c2 = {'Content-Type': 'application/json'}

# 上传文件-已解决
# url_c3 = 'http://istio-test-apigateway.mshare.cn/api/account/v3.0/upload'
# data_c3 = ''
# # headers_c3 = {'Content-Type': 'application/json'} 上传文件的header中不能有content-Type 否则会和下面设置的有冲突
# f1 = open("233.jpg","rb")
# file2 = {'file': ('233.jpg', f1, 'image/jpeg', {'Expires': '0'})}

# 发送验证码
# url_c4 = 'http://istio-test-apigateway.mshare.cn/api/account/v3.0/telrandcode'
# data_c4 = {'tel': '13551833814', 'sign':'sec', 'type': 'reg', 'time':int(time.time()), 'areaCode':'+86', 'user_flag': 'user'}

# req = requests.post(url=url_c4, params=data_c4, cookies=cookie2)
# req = requests.get(url=url_c4,params=data_c4,cookies=cookie2)
# print(req.text)
# print(req.status_code)



"""
#sign
now_time = datetime.datetime.now()
time1_str = datetime.datetime.strftime(now_time, '%Y/%m/%d %H:%M:%S')
print(time1_str)

mobile='18782950041'

kk='bQWv@&Ez6DF*STW4BRo8sjDatrf@5n$i772sKq87AriERG3UxoF*aH%5d#8Aq&Vm'
sign="tel=" + mobile + "&time=" + Custom_p. + "&key=" + kk
print(sign)

m = hashlib.md5()
m.update(sign.encode())
sec = m.hexdigest()
print('sec:',sec)

sec = Custom_p.get_sign(18782950041)
print('sec::::',sec)


#时间戳
t=datetime.datetime.now()
t1 =t.strftime('%Y-%m-%d %H:%M:%S')
start_time=time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))
print('时间戳 %s' %  start_time)


#获取验证码
url='http://istio-test-apigateway.mshare.cn/api/account/v2.0/telrandcode'
type=['reg','pwd','bind','login','mod']
#学生账户
data={'tel':'18782950020','sign': Custom_p.get_sign(18782950020),'type':type[4],'time': Custom_p.get_now_timestamp(),'areaCode':'+86','user_flag':'user'}
#企业账户
data2={'tel':'18782950001','sign': 'Custom_p.get_sign(18782950001)','type':'login','time': 'Custom_p.get_now_timestamp()','areaCode':'+86','user_flag':'company'}
# print('data %s' % data)
# res = requests.get(url,params=data).text
# print('验证码 %s' % res)
# time.sleep(2)

#验证码是否正确
url4='http://istio-test-apigateway.mshare.cn/api/account/v3.0/telrandcode'
data4={'areaCode':'+86','tel':'18782950020','rdcode':'123456','rdid':'1'}
# req = requests.post(url=url4,data=data4,headers=header2).text
# print('验证码是否正确 %s' % req)

data_n = change_custom_param(data2)
print(data_n)

req = requests.get(url=url, params=data_n)
print(req.text)



url5 = 'http://istio-test-apigateway.mshare.cn/api/account/v3.0/cityhistory'
data5 = {'city': '成都'}
data55 = 'city=成都'
data555 = '{"city":"成都"}'

req5 = requests.post(url=url5, data=data555.encode('utf-8'), cookies=cookie2, headers=header1)
print(req5.text)
print(req5.status_code)

url6 = 'http://service.xiaocai.caixuetang.cn/index.php'
data6 = 'c=Traincamp&a=list&v=app&site=traincamp&appcode=5e746cf3a2095l855swnxafe'
data66 = {'c': 'Traincamp', 'a': 'list', 'v': 'app', 'site': 'traincamp', 'appcode': '5e746cf3a2095l855swnxafe'}
req6 = requests.get(url=url6,params=data6)
"""

ad_list = [{'ad_position':'P_10_11','max_num':10},{'ad_position':'P_10_6','max_num':1},{'ad_position':'P_10_43','max_num':10},{'ad_position':'P_10_10','max_num':1}]
url7 = 'http://istio-test-apigateway.mshare.cn/api/account/v3.0/get/media'
data7 = {"city": "全国",
        "client_type": "app",
        "ad_groups": json.dumps(ad_list),
        "client_os": "ios-4.1.2"}

req7 = requests.post(url=url7,data=data7,cookies=cookie2)
print(req7.text)
print(req7.status_code)






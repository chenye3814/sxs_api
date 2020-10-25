
# -*- coding:utf8 -*-

import os,sys
import datetime
BASE_PATH = os.path.dirname(
   os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0,BASE_PATH)             #这个作用可以在其他环境中运行，手动加入环境变量

from IR.lib.common import OpCase
from IR.lib.send_mail import sendmail
from IR.conf import setting
from IR.lib.ClassLogin import ClassLogin
from IR.lib.to_html import *
import json
import string
from IR.lib.Custom_param import Custom_p

class CaseRun(object):
   def find_cases(self,env1):
      op = OpCase()  #实例化
      start = ClassLogin()
      nowtime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 获取当前时间
      result_file_folder = os.path.join(setting.RESULT_PATH, nowtime)  # 拼接文件夹路径
      os.mkdir(result_file_folder)  # 创建文件夹
      result_file_list=[]
      pass_count,fail_count = 0,0   #统计成功失败用例
      print('这是env1=%s' % env1)
      env=json.loads(env1)
      print('这是env=%s' % env)
      for f in os.listdir(setting.CASE_PATH):#每次循环的时候读一个excel
         abs_path = os.path.join(setting.CASE_PATH,f)  #拼接绝对路径
         case_list = op.get_case(abs_path)  #获取每个list中case
         res_list = []
         sys_way0,url0,uri0,method0,req_data0,is_login0,check0,schema= case_list[0] #获取登录信息
         #url0 = setting.DICT_URL.get(url0)
         print('这是url0=%s' % url0)
         print('这是req_data0=%s' % req_data0)
         print('这是case_list[0]=%s' % case_list[0])
         # url0 = env.get(url0) #zyl
         # print(url0) #zyl
         cookie = start.login(url0+uri0,req_data0) #调用完接口返回的结果
         print('这是cookie=%s' % cookie)
         #status0 = op.check_res(cookie, check0)  # 校验结果
         #res_list.append([cookie, status0])  # 结果存入list中
         result_status = ''
         for case in case_list[1::]:#循环每个excel里面所有用例
            sys_way,url,uri,method,req_data,is_login,check,schema = case   #用多个变量接函数结果
            print('这是case=%s' % case)
            #url=setting.DICT_URL.get(url)
            # url = env.get(url) #zyl
            #print('这是url=%s' % url)
            res = op.my_request(sys_way,url+uri,method,req_data,is_login,cookie) #调用完接口返回的结果

            print('这是res=%s' % res)

            if schema:
               status = op.check_json(res, schema)  # 校验结果json格式校验
            else:
               status = op.check_res(res, check)  # 校验结果
            res_list.append([res,status])  #结果存入list中
            if status=='通过':   #循环每次判断
               pass_count+=1
            else:
               fail_count+=1
               result_status ='fail'
         result_file_path=os.path.join(result_file_folder,result_status+f) #拼接结果路径
         result_file_list.append(result_file_path)
         op.write_excel(res_list,result_file_path)  #写入excel  放在循环外面最后写一次就可
         msg = '''
         xx你好：
            本次共运行%s条用例，通过%s条，失败%s条。
         '''%(len(res_list),pass_count,fail_count)
         #sendmail('测试用例运行结果',content=msg,attrs=abs_path)
         html_file_path=os.path.join(result_file_folder,'result.html')
      return pass_count,fail_count,html_file_path,result_file_list


# str_1=sys.argv[1]
# pass_count,fail_count,html_file_path,result_file_list=CaseRun().find_cases(str_1)  #检查是否可用
#
# total_num=pass_count+fail_count
# msg = '''
#          xx你好：
#             本次共运行%s条用例，通过%s条，失败%s条。
#          '''%(total_num,pass_count,fail_count)
# #html_list=excel_sheet_processor(result_file_list)
# #dom=list_diction_to_html(html_list)
# #save_dom_to_html(dom,html_file_path)
# sendmail('测试用例运行结果',content=msg,attrs=result_file_list)#发送报告

#str_1='{"URL_1": "http://istio-test-apigateway.mshare.cn","URL_2": "https://tv.shixiseng.com"}'
str='{"URL_1": "http://istio-test-apigateway.mshare.cn"}'
cr=CaseRun()
pass_count,fail_count,html_file_path,result_file_list=cr.find_cases(str)
#pass_count,fail_count,html_file_path,result_file_list=CaseRun().find_cases(str_1)  #检查是否可用
total_num=pass_count+fail_count
print('本次共运行%s条用例，通过%s条，失败%s条'  % (total_num,pass_count,fail_count))

msg = '''
         xx你好：
            本次共运行%s条用例，通过%s条，失败%s条。
         '''%(total_num,pass_count,fail_count)
html_list=excel_sheet_processor(result_file_list)
dom=list_diction_to_html(html_list)
save_dom_to_html(dom,html_file_path)
#sendmail('测试用例运行结果',content=msg,attrs=result_file_list)#发送报告

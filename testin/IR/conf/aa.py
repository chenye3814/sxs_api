#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : jsonUtil.py
# @Author: Lcy
# @Date  : 2018/8/16
# @Desc  :

from tkinter import *
import json
import sys

#sys.setrecursionlimit(1000000)


class My_GUI():

    def __init__(self):
        self.window = Tk()

        # 设置主窗口属性(窗口名, 大小, 位置, 背景色等)
        self.window.title('JSON处理工具')
        # window.geometry('800x600+50+50')
        self.window['bg'] = 'GhostWhite'
        self.window.attributes('-alpha', 1)

        # 添加两个文本框
        self.input_text = Text(self.window)
        self.input_text['bg'] = 'pink'
        self.input_text.grid(row=0, column=0, sticky=W)

        self.result_labe = Text(self.window)
        self.result_labe['bg'] = 'blue'
        self.result_labe.grid(row=0, column=2)

        self.to_json_button = Button(self.window, text='to_json', bg='lightblue', width=10, command=self.to_json)
        self.to_json_button.grid(row=1, column=1)

        self.window.mainloop()

    # def set_window(self, window):
    def to_json(self):

        self.result_labe.delete(0.0, END)


        def to_jsonschema(json_data, result):

            if isinstance(json_data, dict):
                is_null = True
                require_list = []
                result.append('{')
                result.append("'type': 'object',")
                result.append("'properties': {")
                for k, v in json_data.items():
                    is_null = False
                    result.append("'%s':" % k)
                    print(1, result)
                    to_jsonschema(v, result)
                    result.append(',')
                    require_list.append("'%s'," % k)
                print(33, require_list)
                if not is_null:
                    result.pop()
                    print(2, result)
                result.append('},')
                result.append("'required':[")
                result.extend(require_list)
                result.append("]")

                result.append('}')
            elif isinstance(json_data, bool):
                result.append("{")
                result.append("'type': 'boolean'")
                result.append('}')
            elif isinstance(json_data, list):
                result.append('{')
                result.append("'type': 'array',")
                result.append("'items': ")
                to_jsonschema(json_data[0], result) #注释之前写的
                #to_jsonschema(json_data, result) #修改写法
                result.append('}')
            elif isinstance(json_data, int):
                result.append("{")
                result.append("'type': 'integer'")
                result.append('}')
            elif isinstance(json_data, float):
                result.append("{")
                result.append("'type': 'float'")
                result.append('}')
            elif isinstance(json_data, str):
                result.append("{")
                result.append("'type': 'string'")
                result.append('}')

            return "".join(result)

        json_data = self.input_text.get(0.0, END).strip().replace("\n", "").replace("true","True").replace("false","False")
        result = []
        try:
            testdata = to_jsonschema(eval(json_data), result)
            params = eval(testdata)
            self.result_labe.insert(1.0, json.dumps(params, indent=4))
        except Exception as e:
            self.result_labe.insert(1.0, e)
        # testdata = to_jsonschema(eval(json_data), result)
        # params = eval(testdata)
        # self.result_labe.insert(1.0, json.dumps(params, indent=4))

my_gui = My_GUI()
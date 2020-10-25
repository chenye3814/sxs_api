#!/usr/bin/python
# -*- coding:utf8 -*-
import logging,dominate, sys, os
from xlrd import open_workbook
from dominate.tags import *
# 创建获取excel数据的函数
def excel_sheet_processor(file_list):
    # 创建2个空列表用于储存数据
    workbook_list = []
    my_keys = []
    #遍历文件列表：
    for item in file_list:
        # 通过open_workbook函数 获取Book对象
        wb = open_workbook(item, formatting_info=True)
        # 创建一个新的sheet 对象
        ws = wb.sheet_by_index(0)
        # 通过遍历ncols 获取excel表中第一行（python中0是第一行的意思）和所有列的数据
        if not my_keys:
            for col in range(ws.ncols):
                my_keys.append(ws.cell_value(rowx=0, colx=col))

        # 通过遍历nrows和 获取excel表中所有行里面的和对应列的数据
        for r in range(1,ws.nrows):
            dict = {}
            for pos in range(0, len(my_keys)):
                dict[my_keys[pos]] = ws.cell_value(rowx=r, colx=pos)
            # 将获取的字典数据  添加进一开始写好的空列表中
            workbook_list.append(dict)
    return workbook_list


# 创建excel生成静态html页面的函数
def list_diction_to_html(list_work):
    # 用dominate函数生成静态html页面
    doc = dominate.document(title='excel-to-html')
    # 写在头部的 css 可以自定义自己的想要用的css文件， （重要： meta一定要加 要不会在打开html时乱码，因为html默认不是utf-8编码）
    with doc.head:
        link(rel='stylesheet', href='Perconnel/static/css/style.css', style='width: 50px')
        meta(charset='utf-8')
    # 创建一个table，将获取到的数据通过遍历添加进去对应的位置
    with doc:
        with div(id='excel_table').add(table()):
            with thead():
                dict = list_work[0]
                for key in dict.keys():
                    table_header = td()
                    table_header.add(p(key))
            for dict2 in list_work:
                table_row = tr(cls='excel_table_row')
                for key in dict2:
                    with table_row.add(td()):
                        p(dict2[key])
    return str(doc)


# 合并多个excel文件生成html
def merge_excel_to_list(file_list):
    dict_list=[]
    data_list=[]
    for item in file_list:
        temp_list=excel_sheet_processor(item)
        data_list.append(temp_list)
    return data_list


# 保存生成后html的函数
def save_dom_to_html(dom,filepath):
    #filepath = os.path.abspath(filepath)
    htmfile = open(filepath, "w",encoding="utf-8")
    htmfile.write(dom)
    htmfile.close()
    return filepath

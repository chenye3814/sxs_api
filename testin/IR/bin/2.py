import json


# a = [{'ad_position':'P_10_11','max_num':10},{'ad_position':'P_10_6','max_num':1},{'ad_position':'P_10_43','max_num':10},{'ad_position':'P_10_10','max_num':1}]
# b = json.dumps(a)
# print(type(b))
# print(b)
#
# c = [1,2,3,4]
# d = json.dumps(c)
# print(type(d))
# print(d)

def test2(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} == {value}')


test2(name='张三')

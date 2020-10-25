import hashlib
import time
import datetime

class Custom_p():
    def __init__(self):
        pass

    @staticmethod
    def now_time():
        """获取格式化当前时间"""
        now_time = datetime.datetime.now()
        time1_str = datetime.datetime.strftime(now_time, '%Y/%m/%d %H:%M:%S')
        return time1_str

    @staticmethod
    def get_sign(tel):
        """通过电话号码生成sign参数"""
        mobile = str(tel)
        kk = 'bQWv@&Ez6DF*STW4BRo8sjDatrf@5n$i772sKq87AriERG3UxoF*aH%5d#8Aq&Vm'
        sign = "tel=" + mobile + "&time=" + Custom_p.now_time() + "&key=" + kk
        m = hashlib.md5()
        m.update(sign.encode())
        sec = m.hexdigest()
        return sec

    @staticmethod
    def get_now_timestamp():
        """获取当前时间的时间戳"""
        t = datetime.datetime.now()
        t1 = t.strftime('%Y-%m-%d %H:%M:%S')
        start_time = time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))
        return start_time


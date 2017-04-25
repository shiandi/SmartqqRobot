# -*- coding: utf-8 -*-
__author__ = 'lius'

import tkinter
import requests
import random
import time
# import re
from multiprocessing import Process
# import threading

class SmartQQRobot():
    def __init__(self,qq_number):
        self._qq_number = qq_number
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}

        self._session = requests.session()
        self._session.headers.update(self._headers)
        self._cookies_qrsig = ""

        self._login_status = False

    def _show_QRC(self,content):
        if(content != None):
            root = tkinter.Tk()  #显示二维码
            root.title("扫描二维码")
            root.geometry('200x150') #设置窗口大小
            root.resizable(width=False, height=False) #窗口大小不可变
            img = tkinter.PhotoImage(data=content)
            label = tkinter.Label(root, image=img)
            label.pack()
            root.mainloop()
        else:
            # self._login_error = True
            print("二维码获取失败.")

    def _get_ptqrtoken(self):
        # ptqrtoken 计算
        token = 0
        for i in range(len(self._cookies_qrsig)):
            token += (token << 5) + ord(self._cookies_qrsig[i])
        print(2147483647 & token)
        return 2147483647 & token

    def _check_login_status(self):
        url = "https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=" + str(self._get_ptqrtoken()) +\
              "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106" \
              "&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10" \
              "&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert" \
              "&action=0-0-" + str(random.randint(1000, 30000)) +\
              "&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10216&login_sig=&pt_randsalt=2"
        print(url)
        # 死循环检测扫码登陆状态
        while 1:
            content = self._session.get(url=url).content.decode("utf-8")
            print(content)
            # 登陆成功跳出循环
            if "ptuiCB" not in content:
                self._login_status = True
                break
            time.sleep(3)

    def _login(self):
        url = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&amp;e=0&amp;l=M&amp;s=5&amp;d=72&amp;v=4&amp;t=0.6228904674882688"
        content = self._session.get(url=url).content  #获取二维码数据（二进制）
        self._cookies_qrsig = (requests.utils.dict_from_cookiejar(self._session.cookies))["qrsig"]
        #使用进程显示二维码，等待扫描。
        p = Process(target=self._show_QRC,args=(content,))
        #启动进程 p
        p.start()
        time.sleep(1)
        self._check_login_status()
        # 结束进程 p
        if p.is_alive():
            p.terminate()


    def msg_robot(self):
        pass

    def run(self):
        self._login()

if __name__=="__main__":
    qq = SmartQQRobot(111)
    qq.run()
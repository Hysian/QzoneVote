#coding:utf-8
import Queue
import random

import re
import requests
import threading
from g_tk import getNewGTK,getOldGTK
from cookies import cookies
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from word import word1


quit_flage = False
pq = Queue.Queue()

def que_print(msg):
    pq.put(msg)
def print_thread():
     while not (quit_flage and pq.empty()):  # 当队列为空且退出标记为True时结束循环
        try:
            msg = pq.get(True, 0.1)           # 从队列中取出一个元素，最多阻塞0.1秒
        except Queue.Empty:                  # 队列空，进入下一个循环
            continue
        print msg

class zone:
    def __init__(self):
        self.head1 = {
                 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                 'Accept-Encoding': 'gzip, deflate',
                 'Connection': 'keep-alive',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv',
                 'Host': 'ptlogin2.qq.com',
                 'Referer': 'http://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=http%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=http%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html'
                 }
        self.qqlist = []
        self.s = requests.Session()
    def getTk(self):
        tcookies = self.s.cookies.get_dict()
        p_skey = tcookies['p_skey']
        skey = tcookies['skey']
        rv2 = None
        g_tk = getNewGTK(p_skey, skey, rv2)
        self.g_ok = getOldGTK(skey)
        return str(g_tk)
    def login(self):
        self.s.cookies.update(cookies)
        self.qq = self.s.cookies['uin'].rsplit('o0')[1]
        self.g_tk = self.getTk()
    def addms(self,uid):
        self.s.headers['Host'] = 'm.qzone.qq.com'
        url = u'http://m.qzone.qq.com/cgi-bin/new/add_msgb?g_tk='+self.g_tk
        txt = random.sample(word1, 5)
        for x in txt:
            form = {
                    'qzreferrer': "http://qzs.qq.com/qzone/msgboard/msgbcanvas.html#page=1",
                    'content': x,
                    'hostUin': uid,
                    'uin': self.qq,
                    'format': "fs", 'inCharset': "utf-8",'outCharset': "utf-8", 'iNotice': "1", 'ref': "qzone",'json': "1",
                    'g_tk': self.g_tk
                    }
            con = self.s.post(url, data=form).content
            f = re.findall(u'"message":"(.*)",', con)[0]
            que_print(u'%s--> %s'%(uid, x))
        return f

def main(qq):
    t = threading.Thread(target=print_thread)
    t.start()
    p = zone()
    p.login()
    n = 0
    while True:
        f = p.addms(qq)
        if f == '空间主人设置了回复权限，您无法进行操作':
            que_print(f)
            break
        if f == '操作过于频繁咯！休息会再来操作吧！':
            que_print(f)
            time.sleep(60)
        n += 1
    t.join()

main("qq")

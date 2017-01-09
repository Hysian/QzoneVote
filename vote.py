#coding:utf-8
import random
import re
import subprocess
import Queue
import requests
import time
import word
import threading
from g_tk import getNewGTK, getOldGTK
from cookies import cookies
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

pq = Queue.Queue()
resq = Queue.Queue()
flage = False
newqq = []

def que_print(msg):
    pq.put(msg)

def print_thread():
     while not (flage and pq.empty()):  # 当队列为空且退出标记为True时结束循环
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

    def getShow(self):
        self.s.headers.update(self.head1)
        parm = {'e': '2', 'd': '72', 'daid': '5', 'appid': '549000912', 'l': 'M', 's': '3', 'v': '4','t': random.random()}
        ptqurl = "http://ptlogin2.qq.com/ptqrshow"
        con = self.s.get(ptqurl, params=parm).content   #获取二维码
        with open('im.png','wb') as f:
            f.write(con)
        subprocess.call('im.png',shell=True)            #打开二维码图片
        while True:
            parm = {
                    'action': int(time.time()*1000),
                    'ptredirect': '0', 'pt_uistyle': '40',
                    'g': '1', 'ptlang': '2052',
                    'js_type': '1', 'h': '1', 'daid': '5',
                    't': '1', 'from_ui': '1', 'js_ver': '10191', 'aid': '549000912',
                    'u1': 'http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone'
                    }
            forl = "http://ptlogin2.qq.com/ptqrlogin"
            succjs = self.s.get(forl, params=parm).content
            que_print(succjs)
            time.sleep(2)
            if len(self.s.cookies) > 1:             #登陆认证返回多个cookie，结束循环
                que_print(u'登陆成功')
                break
        self.s.headers['Host'] = "ptlogin4.qzone.qq.com"
        st1 = re.findall(u'(http.*),\'0', succjs)[0]
        self.s.get(st1)
        self.getTk()
        txt = 'cookies = '+str(self.s.cookies.get_dict())
        self.qq = self.s.cookies['uin'].rsplit('o0')[1]
        with open('cookies.py', 'w') as co:        #保存新cookies
            co.write(txt)

    def getTk(self):
        tcookies = self.s.cookies.get_dict()
        p_skey = tcookies['p_skey']
        skey = tcookies['skey']
        g_tk = getNewGTK(p_skey, skey, None)
        self.g_ok = getOldGTK(skey)
        self.g_tk = str(g_tk)

    def login(self):
        self.s.cookies.update(cookies)
        self.qq = self.s.cookies['uin'].rsplit('o0')[1]
        self.getTk()

    def add_msg(self, flag):
        self.s.headers['Host'] = 'm.qzone.qq.com'
        url = u'http://m.qzone.qq.com/cgi-bin/new/add_msgb?g_tk='+self.g_tk
        while True:
            txt = random.sample(word.word1, 3)
            if flag == 1:
                time.sleep(2)
                uid = str(q.get())
                que_print(u'当前点赞%s'  %newqq)
                que_print(u'已点赞%s'    %self.qqlist)
                que_print(u'取出 --->%s' %uid)
            else:
                time.sleep(60)
                uid = str(resq.get())
                que_print(u'重复 --->%s' %uid)
            # que_print(u'队列长度%d' %q.qsize())
            for ly in txt:
                form = {'qzreferrer': "http://qzs.qq.com/qzone/msgboard/msgbcanvas.html#page=1",
                        'content': ly, 'hostUin': uid, 'uin': self.qq, 'g_tk': self.g_tk,
                        'format': "fs", 'inCharset': "utf-8",'outCharset': "utf-8", 'iNotice': "1", 'ref': "qzone",'json': "1",
                        }
                try:
                    po = self.s.post(url, data=form)
                    f = re.findall(u'"message":"(.*)",', po.content)[0]
                    f = ''
                    que_print(u'%s--_---%s' %(uid, ly))
                except Exception, e:
                    print po.content
                    que_print(u'%s错误---%s' %(str(Exception), e))
                    resq.put(uid)
                    break
                if f == '空间主人设置了回复权限，您无法进行操作':
                    que_print(f)
                    break
                if f == '操作过于频繁咯！休息会再来操作吧！':
                    resq.put(uid)
                    que_print(f)
                    break
            if flag == 2:
                resq.task_done()
            else:
                q.task_done()

    def getShuo(self):
        s = self.s
        s.headers['Host'] = 'taotao.qq.com'
        s.headers['Referer'] = "http://user.qzone.qq.com/609647489/main"
        parm = {'uin': self.qq, 'ftype': '0', 'sort': '0','pos': '0', 'num': '20', 'replynum': '100', 'g_tk': self.g_ok,'callback': '_preloadCallback', 'code_version': '1', 'format': 'jsonp', 'need_private_comment': '1'}
        con = s.get('http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6', params=parm).content
        textlist = re.split('\{"certified"', con)[1:]
        tid = re.findall('"t1_termtype":.*?"tid":"(.*?)"', textlist[0])[0]
        return tid

    def getVote(self, tid):
        while True:
            try:
                if len(self.qqlist) < 15:
                    url = 'http://r.qzone.qq.com/cgi-bin/user/qz_opcnt2?_stp=1455969198161&unikey=http%3A%2F%2Fuser.qzone.qq.com%2F'+self.qq+'%2Fmood%2F'+tid+'.1%3C.%3Ehttp%3A%2F%2Fuser.qzone.qq.com%2F'+self.qq+'%2Fmood%2F'+tid+'.1&face=0&fupdate=1&g_tk=' + str(self.g_ok)
                    vote = self.s.get(url).content
                    newqq = re.findall('\[(\d*),', vote)
                else:
                    voteurl = 'http://users.qzone.qq.com/cgi-bin/likes/get_like_list_app?uin='+self.qq+'&unikey=http://user.qzone.qq.com/'+self.qq+'/mood/'+tid+'&begin_uin=0&query_count=60&if_first_page=1&g_tk='+self.g_tk
                    self.s.headers['Host'] = 'users.qzone.qq.com'
                    self.s.headers['Referer'] = "http://user.qzone.qq.com/"+self.qq+"/311"
                    vote = self.s.get(voteurl).content
                    newqq = re.findall('"fuin":(\d+),', vote)
                new = list(set(newqq).difference(set(self.qqlist)))
                for qq in new:
                    q.put(qq) #将点赞qq放入队列
                    que_print(u'存入 <---%s'%qq)
                    self.qqlist.append(qq)
                time.sleep(1)
            except:
                continue

if __name__ == '__main__':
    t = threading.Thread(target=print_thread)
    t.start()
    q = Queue.Queue()
    p = zone()
    p.getShow()
    count = 0

    with open('id.txt','r+') as f:
        oldId = f.read()
    while True:
        newId = p.getShuo()
        if newId != oldId:
            with open('id.txt','w') as f:
               f.write(newId)
            que_print('已更新说说')
            break
        if count%5 == 1:
            que_print('未发布说说')
        time.sleep(1)

    t1 = threading.Thread(target=p.getVote, args=(newId,))
    t2 = threading.Thread(target=p.add_msg, args=(1,))
    res = threading.Thread(target=p.add_msg, args=(2,))

    res.start()
    t1.start()
    t2.start()

    t.join()
    t1.join()
    t2.join()
    res.join()

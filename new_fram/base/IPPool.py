#! usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Kwinner Chen'


from queue import Queue
from multiprocessing import Queue as mqueue
from multiprocessing.managers import BaseManager
from multiprocessing import Process
from threading import Thread
from time import sleep
from random import random
import requests
import re


class IPPool(Queue):
    '''
    实例化时生成一个自更新的代理IP列队
    '''

    def __init__(self, conn=None, ipurl=None):
        '''
        本身就是一个queue消息列队
        :params:
        :conn: 一个消息列队链接实例，用于在运行中接收用于更新的代理ip地址。原则上可以使用通道pipe
        :ipurl: 代理IP地址，可以在初始化时传入，或者在代理列队运行中传入。
        '''

        super().__init__()
        self.ipurl = ipurl or 'http://vip22.xiguadaili.com/ip/?tid=556082430314945&num=1000&category=2&protocol=https'
        if conn:
            self.conn = conn
            t_ = Thread(target=self.__refresh_ipurl)
            t_.start()
        t = Thread(target=self.__refresh)
        t.start()
        

    def __refresh_ipurl(self):
        # 监控用于跟新代理地址的列队是否有新消息
        # 只需改变自身ipurl属性
        while True:
            if not self.conn.empty():
                url = self.conn.get()
                self.ipurl = url
                print('链接更新成功！')
            sleep(random()*5)

    def __refresh(self):
        # 当自身列队为空时进行更新操作
        while True:
            if self.empty():
                self.__local_refresh()
            else:
                print('当前代理个数为: %04d' % self.qsize(), end='\r')
                sleep(random()*5)

    def __local_refresh(self):
        header = header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        try:
            resp = requests.get(self.ipurl, headers=header)
            text = resp.text
            iplist = re.findall(r'((?:(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:\d{1,2}|1\d{2}|2[0-4]\d|25[0-5]):\d+)', text)
        except:
            iplist = None
        if iplist:
            for ip in iplist:
                self.put({'https':'https://%s'%ip})
        else:
            print('订单过期或出现网络错误，无法更新代理池！请检查后运行refresh_ipurl(url)替换链接或恢复链接！') 


class IPPoolManager:
    '''代理池管理，用于启动、获取代理池，并在代理池过期后更新代理URL。
       服务端：初始化IPPoolManager，运行run_server()使列队进入入伍状态。
       应用端：实例化IPPoolManager，运行get_ippool获取代理列队。
       '''

    def __init__(self, ip='localhost', port=16000, authkey='ippool'):
        '''
        :params:
        :ip: 代理列队注册服务器的ip地址
        :port: 分配给代理列队的端口号，默认为16000
        :authkey: 代理列队口令，一般使用默认值
        '''

        self.ip = ip
        self.port = port
        self.authkey = authkey

    def run_server(self, ipurl=None):
        '''
        已ipurl为代理地址运行一个代理列队服务。
        '''

        p = Process(target=self.inner_q)
        p.start()
        class MyManager(BaseManager): pass
        manager = MyManager((self.ip, self.port), self.authkey.encode('utf-8'))
        conn = self.inner_get_q()
        q = IPPool(conn=conn, ipurl=ipurl)
        print('成功获取到代理列队！')
        manager.register('get_ippool', callable=lambda: q)
        print('创建服务...')
        server = manager.get_server()
        print('成功创建代理池服务！')
        print('代理池运行中...')
        server.serve_forever()

    def get_ippool(self):
        '''
        获取运行的代理列队
        '''
        
        class MyManager(BaseManager): pass
        manager = MyManager((self.ip, self.port), self.authkey.encode('utf-8'))
        manager.register('get_ippool')
        manager.connect()
        return manager.get_ippool()

    def refresh_ipurl(self, url):
        '''
        用于更新代理地址，需要在新进程中运行
        >>> ippoolmanager = IPPoolManager()
        >>> ippoolmanager.refresh_ipurl(someurl)
        '''

        print('链接代理服务...')
        q = self.inner_get_q()
        print('成功获取到列队！')
        q.put(url)
        print('成功添加', url, '到服务！')

    def inner_q(self):
        # 注册并运行一个内部使用的用于更新代理地址的列队
        class innerManager(BaseManager): pass
        q = mqueue(1)
        manager = innerManager((self.ip, self.port+1), self.authkey.encode('utf-8'))
        manager.register('get_q', callable=lambda: q)
        server = manager.get_server()
        server.serve_forever()

    def inner_get_q(self):
        # 获取用于更新代理地址的消息列队
        class innerManager(BaseManager): pass
        manager = innerManager((self.ip, self.port+1), self.authkey.encode('utf-8'))
        manager.register('get_q')
        manager.connect()
        return manager.get_q()

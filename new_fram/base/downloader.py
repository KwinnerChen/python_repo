#! usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Kwinner Chen'


import requests
from .configmodul import Config


class Donlowder:
    '''
    下载器，实例化需定义是否需要代理池
    '''
    
    def __init__(self, session=False, ippool=None):
        self.ippool = ippool
        self.session = requests.Session() if session else requests

    def get_page(self, task):
        assert self.__check_task(task), "重试已超过限定次数！"
        url = task.url
        method = task.method
        kwargs = task.kwargs
        if method.low() == 'get':
            try:
                resp = self.session.get(url=url, **kwargs, proxies=self.ippool.getip() if self.ippool else None)
                resp.raise_for_status
                task.response = resp
                return task, None
            except Exception as e:
                task.times+=1
                return task, e
        elif method.low() == 'post':
            try:
                resp = self.session.post(url=url, **kwargs, proxies=self.ippool.getip() if self.ippool else None)
                resp.raise_for_status
                task.response = resp
                return task, None
            except Exception as e:
                task.times += 1
                return task, e
                
    def __check_task(self, task):
        _times = getattr(task, 'times', 0)
        if _times>Config.RETRY_TIMES.value:
            return 0
        else:
            return 1

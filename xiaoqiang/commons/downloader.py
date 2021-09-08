#! usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Kwinner Chen'


from log import Logger
import requests
from task import Task
from utils import import_module


class Donlowder:
    '''
    下载器，完成Task对象规定的下载任务。
    '''
    
    def __init__(self, *, session=False, max_retry=0, mdws=[]):
        """
        :params:
        :session: bool, 是否使用Session会话；
        :max_retry: int, 错误重试次数，<0不限次数，==0默认值只请求一次，>0则重试相应次数；
        :mdws: list， 请求中间件，在发送请求前预先处理请求任务，例如使用IP代理。
        """
        self.session = requests.Session() if session else requests
        self.max_retry = max_retry
        self.mdws = mdws
        self.logger = Logger(self.__class__.__name__)

    def get_page(self, task):
        if self.max_retry < 0:
            while True:
                resp, err = self.__get_page__inner(task)
                if err is None:
                    return resp, None
        
        elif self.max_retry == 0:
            return self.__get_page__inner(task)
        
        else:
            for _ in range(self.max_retry):
                resp, err = self.__get_page__inner(task)
                if err is None:
                    return resp, None
            return resp, err
        

    def __get_page__inner(self, task):
        task = self.__mdws_process(task)

        if task.method.lower() == 'get':
            return self.get(task)
        elif task.method.lower() == 'post':
            return self.post(task)

    def get(self, task:Task):
        try:
            resp = self.session.get(url=task.url, **task.kwargs)
            resp.raise_for_status()
            if task.delayitem:
                resp.delayitem = task.delayitem
            return resp, None
        except Exception as e:
            return None, e
        
    def post(self, task:Task):
        try:
            resp = self.session.post(url=task.url, **task.kwargs)
            resp.raise_for_status()
            if task.delayitem:
                resp.delayitem = task.delayitem
            return resp, None
        except Exception as e:
            return None, e

    def __mdws_process(self, task):
        for mdw in self.mdws:
            task = mdw.process(task)
        return task

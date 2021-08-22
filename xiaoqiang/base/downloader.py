#! usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Kwinner Chen'


from collections import defaultdict

import requests

from base.task import Task


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
        self.__retry_times_map = defaultdict(int)

    def get_page(self, task):
        task_hash = hash(task)
        assert self.__check_task(task, task_hash), "重试已超过限定次数！"
        task = self.__mdws_process(task)
        method = task.method

        if method.low() == 'get':
            return self.get(task, task_hash)
        elif method.low() == 'post':
            return self.post(task, task_hash)

    def get(self, task:Task, task_hash):
        try:
            resp = self.session.get(url=task.url, **task.kwargs)
            resp.raise_for_status()
            if task.delayitem:
                resp.delayitem = task.delayitem
            return resp, None
        except Exception as e:
            self.__retry_times_map[task_hash] += 1
            return None, e
        
    def post(self, task:Task, task_hash):
        try:
            resp = self.session.post(url=task.url, **task.kwargs)
            resp.raise_for_status()
            if task.delayitem:
                resp.delayitem = task.delayitem
            return resp, None
        except Exception as e:
            self.__retry_times_map[task_hash] += 1
            return None, e

    def __mdws_process(self, task):
        for mdw in self.mdws:
            task = mdw.process(task)
        return task
                
    def __check_task(self, task:Task, task_hash):
        if task.times == 0:
            if self.__retry_times_map[task_hash] <= self.max_retry:
                return True
            else:
                return False
        else:
            if self.__retry_times_map[task_hash] <= task.times:
                return True
            else:
                return False


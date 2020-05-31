#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.getcwd())
from base.task import Task
import abc


class BaseSpider(abc.ABC):
    '''
    爬虫类的基类
    :params:
    :name: 爬虫类名，必须定义，用于区别个爬虫，否则无法运行
    :start_urls: 起始链接的列表，可以为空，同时定义一个start_request方法
    :response_parser: 用于解析start_request返回的响应对象，必须定义，该方法返回一个任务对象或者item对象
    '''
    name = ''
    start_urls = []

    def start_request(self):
        assert self.start_urls, "若没有重新定义start_request方法，则必须定义start_urls类变量！"
        for url in self.start_urls:
            yield Task(url=url, callback=self.response_parser)
    
    @abc.abstractmethod
    def response_parser(self, response, item):
        pass
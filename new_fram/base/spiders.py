#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#TODO:编写爬虫类的元类，检查定义爬虫类时，必须定义的属性是否已经定义


from .task import Task
import abc


class SpiderMeta(type):
    """
    爬虫类的元类，对每个爬虫类的定义进行检查，防止必须定义的属性没被定义
    """
    def __new__(cls, names, attr_dict):
        if 'name' not in attr_dict:
            raise KeyError("类参数 name 是必须定义的，它是用以区别爬虫类的唯一标志！")
        elif "name" == "":
            raise KeyError("类参数 name 应该定义为有意义且唯一的，否则无法用于区分不同的爬虫类！")


class BaseSpider(abc.ABC, metaclass=SpiderMeta):
    '''
    爬虫类的基类
    :params:
    :name: 爬虫类名，必须定义，用于区别个爬虫，否则无法运行
    :start_urls: 起始链接的列表，可以为空，同时定义一个start_request方法
    :response_parser: 用于解析start_request返回的响应对象，必须定义，该方法返回一个任务对象或者item对象
    '''
    name = ''
    start_urls = []

    def __init__(self) -> None:
        self.init()

    def init(self):
        pass

    def start_request(self):
        assert self.start_urls, "若没有重新定义start_request方法，则必须定义start_urls类变量！"
        for url in self.start_urls:
            yield Task(url=url, callback=self.response_parser)
    
    @abc.abstractmethod
    def response_parser(self, response):
        pass
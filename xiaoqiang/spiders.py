#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Kwinner Chen'

'''
此处定义爬虫的解析代码，爬虫类必须继承BaseSpider爬虫给基类。
需要定义类属性name用于区分每个爬虫。
定义其实链接start_urls <list>或者重写start_request方法，要求该方法返回一个任务对象。
response_parser是必须定义的类方法，他接受一个response响应对象，必须返回一个任务实例或者item实例。
该爬虫给需在setting中进行注册
'''

from commons import BaseSpider
from commons import Item


class Spider(BaseSpider):
    pass
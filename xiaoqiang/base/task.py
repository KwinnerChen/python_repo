#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Task:
    '''
    自定义任务对象，在爬虫任务流中流动。
    :params:
    :url: 请求访问链接
    :method: 请求访问方法，默认为get请求
    :callback: 回调函数，用于解析response响应对象
    :times: 请求次数标记
    :delayitem: 存放缓存，用于多步解析的item
    :kwargs: 该参数将传递给下载器
    '''
    def __init__(self, url, *, method='get', callback=None, times=0, delayitem=None, **kwargs):
        self.url = url
        self.method = method
        self.callback = callback
        self.times = times
        self.delayitem = delayitem
        self.kwargs = kwargs

    def __setattr__(self, name, value):
        if name not in {"url", "method", "callback", "times", "delayitem", "kwargs"}:
            raise AttributeError(f"<{name}>属性未定义，不可随意添加！")
        super().__setattr__(name, value)

    def __repr__(self):
        return f"Task<url:{self.url}, method:{self.method}, callback:{self.callback}, times:{self.times}, delayitem:{self.delayitem}, kwargs:{self.kwargs}>"

    __str__ = __repr__
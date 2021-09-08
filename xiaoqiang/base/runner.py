#! usr/bin/env python3
# -*- coding: utf-8 -*-
# TODO:重构，任务流程已经改变


from argparse import ArgumentParser
from utils import import_module
from log import Logger
from configmodul import Config


class Run:
    """
    运行类，加载所有模块。解析命令行。
    正确处理运行信息和错误信息。
    """
    def __init__(self) -> None:
        # TODO:加载所有运行模块
        argparser = ArgumentParser(
            description="""
            初始化各模块，并启动执行器。
            """
        )
        argparser.add_argument("crawler", type=str, nargs=1, help="指明要启动的爬虫任务，即爬虫定义中的name的值。")
        argparser.add_argument("-H", "--publisher", help="以生产者模式启动，该模式一般指调用爬虫的启动方法，向队列中注入任务。", nargs=0)
        argparser.add_argument("-C", "--consumer", help="以消费者模式启动，该模式将直接从队列中获取任务并运行。", nargs=0)
        self.args = argparser.parse_args()

        downloader_class = import_module(Config.DOWNLOADER)
        executor_class = import_module(Config.EXECUTOR)
        db_class = import_module(Config.STORAGE_MODUL)
        middleware_classes = [import_module(module) for module in Config.MIDDLEWARE]
        crawler_classes = [import_module(module) for module in Config.SPIDERS]
        

        self.logger = Logger(self.__class__.__name__)
        pass


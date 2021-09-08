# -*- coding: utf-8 -*-


"""
执行器，负责主要的执行逻辑。
"""


import functools
import pickle
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

from pika.exceptions import (ChannelClosed, ChannelClosedByBroker,
                             ConnectionClosed, ConnectionClosedByBroker)

from configmodul import Config
from dbs import DBBase
from downloader import Donlowder
from item import ItemBase
from queues import RabbitMQ
from spiders import BaseSpider
from task import Task
from configmodul import Config
from log import Logger


class Executor(ABC):
    """
    执行器基类，所有执行器都继承自该类。
    该类抽象了三个方法，分别对应于三种执行模式：
    以服务模式执行；
    以工作模式执行；
    全模式执行；
    """
    def __init__(self, crawler: BaseSpider, downloader: Donlowder, db: DBBase, config: Config) -> None:
        # spider对象实例
        self.crawler = crawler
        # 配置类
        self.config = config
        # 下载器
        self.downloader = downloader
        # 数据库
        self.db = db
        # 日志记录器
        self.logger = Logger(self.__class__.__name__)

    def run(self, model):
        if model == "all":
            self.execute_as_publisher()
            self.execute_as_consumer()
        elif model == "publisher":
            self.execute_as_publisher()
        elif model == "consumer":
            self.execute_as_consumer()
        else:
            raise Exception("请指定一种工作模式，--server，--worker， --all")

    # 两个函数没有必要全都定义
    @abstractmethod
    def execute_as_publisher(self):
        print(f"--server 执行器没有定义")
        pass

    @abstractmethod
    def execute_as_consumer(self):
        print("--worker 执行器没有定义")
        pass

    def __del__(self):
        self.db.close()


class RabbitExecutor(Executor):
    def __init__(self, crawler: BaseSpider, downloader: Donlowder, db: DBBase, config: Config, logger: Logger) -> None:
        super().__init__(crawler, downloader, db, config, logger)
        self.threadpool = ThreadPoolExecutor(Config.THREAD_NUM)
        self.rabbit = RabbitMQ(**config.QUEUE_CONFIG)
        self.queue_name = crawler.name
        self.exname = self.queue_name.split(".")[0]

    def execute_as_publisher(self):
        while True:
            try:
                # 队列的初始化工作
                connection = self.rabbit.connect()
                channel = self.rabbit.channel()
                self.rabbit.declare_exchange(self.exname)
                self.rabbit.declare_queue(self.queue_name)

                self.__start_crawler()

                return

            except (ConnectionClosed, ChannelClosed):
                continue

            except (KeyboardInterrupt, ConnectionClosedByBroker, ChannelClosedByBroker):
                return

    def execute_as_consumer(self):
        while True:
            try:
                connection = self.rabbit.connect()
                channel = self.rabbit.channel()
                self.rabbit.declare_exchange(self.exname)
                self.rabbit.declare_queue(self.queue_name)

                self.__crawler_consumer()

                return

            except (ConnectionClosed, ChannelClosed):
                continue

            except (KeyboardInterrupt, ConnectionClosedByBroker, ChannelClosedByBroker):
                return

    def __start_crawler(self):
        # 爬虫起始任务
        for task in self.crawler.start_request():
            self.rabbit.publish(
                pickle.dumps(task),
                routing_key=self.queue_name,
                exname=self.exname
            )

    def __crawler_consumer(self):
        # 开始消费队列
        for methodfram, _, body in self.rabbit.consume(self.queue_name):
            delivery_tag = methodfram.delevery_tag
            task = pickle.loads(body)
            # 队列中获取为None时主动停止消费
            if task is None:
                return
            self.threadpool.submit(self.__worker, task, delivery_tag)

    def __worker(self, body, delivery_tag):
        if isinstance(body, Task):
            response, err = self.downloader.get_page(body)
            if err:
                # 请求出错重试在下载模块，这里不再重试
                self.logger.error(f"{body}下载失败：{err}")
            else:
                # 确认任务请求完成
                self.rabbit.add_callback_threadsafe(
                    functools.partial(
                        self.rabbit.basic_nack, delivery_tag
                    )
                )
                # 对请求结果调用回调函数
                result = body.callback(response)
                # 回调返回任务对象加入队列中等待执行
                if isinstance(result, Task):
                    self.rabbit.add_callback_threadsafe(
                        functools.partial(
                            self.rabbit.publish,
                            result,
                            self.queue_name,
                            self.exname
                        )
                    )
                # Item对象则入库
                elif isinstance(result, ItemBase):
                    count = 0
                    while True:
                        count += 1
                        try:
                            self.db.save(result, self.crawler.name)
                            if count > 1:
                                self.logger.warning(f"数据库恢复，{result}已入库。")
                        except Exception as e:
                            if count == 1:
                                self.logger.error(f"数据库错误：{e}，任务{body}解析结果{result}入库失败。")
                            else:
                                self.logger.error(f"数据库错误：{e}，任务{body}解析结果{result}入库失败。", notify=False)
                # 回调返回的也可能是一个任务对象或者Item对象的可迭代对象
                elif isinstance(result, Iterable):
                    for r in result:
                        if isinstance(r, Task):
                            self.rabbit.add_callback_threadsafe(
                                functools.partial(
                                    self.rabbit.publish,
                                    r,
                                    self.queue_name,
                                    self.exname
                                )
                            )
                        elif isinstance(r, ItemBase):
                            count = 0
                            while True:
                                count += 1
                                try:
                                    self.db.save(r, self.crawler.name)
                                    if count > 1:
                                        self.logger.warning(f"数据库恢复，{r}已入库。")
                                except Exception as e:
                                    if count == 1:
                                        self.logger.error(f"数据库错误：{e}，任务{body}解析结果{r}入库失败。")
                                    else:
                                        self.logger.error(f"数据库错误：{e}，任务{body}解析结果{r}入库失败。", notify=False)
                    
                else:
                    # 没有新入伍入队也没有新任务存储
                    self.logger.warning(f"任务:{body}回调函数没有返回应有类型{result}")
                    pass
        else:
            # 队列中的不是任务对象，暂时不用理
            pass


    def __del__(self):
        # 关闭线程池，等待线程中的任务完成
        self.threadpool.shutdown() 
        # 关闭队列，取消消费器，未确认的消息重新入队
        self.rabbit.close()
        # 继承父类的数据库连接池的关闭
        super().__del__

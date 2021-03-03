#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import abc
import pika
import pickle
from threading import Lock
from base.configmodul import Config


# 全局线程锁
Lock = Lock()


class QueueBase(abc.ABC):
     # 链接对象使用单例模式
    connection = None                                         

    # 绑定配置参数
    def __init__(self, configdict:Config, queue_name:str):
        cls = self.__class__                               
        self.queue_name = queue_name
        for k, v in configdict.value.items():
            setattr(self, k, v)
        Lock.acquire()
        if cls.connection is None or cls.connection.is_closed:
            cls.connection = self.connect()
        Lock.release()


    @abc.abstractmethod
    def connect(self):
        """
        定义具体的链接方法，一般在实例化且没有链接实例时执行一次
        """

    @abc.abstractmethod
    def get(self):
        """
        从队列获取一条任务，如果有后续操作，并完成获取任务后的确认等操作，
        返回任务对象
        """

    @abc.abstractmethod
    def put(self, value):
        """
        向队列中推送一条任务对象，如果有后续确认等操作，完成后续操作
        """


class Rabbitmq(QueueBase):

    def __init__(self, configdict, queue_name):
        super().__init__(configdict, queue_name)
        self.channel = None

    # 返回一个链接对象
    # 因为链接对象是单例模式
    # 只有在没有链接对象，或者链接关闭的情况下才
    def connect(self):
        cred = pika.PlainCredentials(self.username, self.password)
        con_params = pika.ConnectionParameters(host=self.host, port=self.port, 
                                                    virtual_host='/', credentials=cred)
        connection = pika.BlockingConnection(con_params)
        return connection
              
    # rabbitmq的链接对象是非线程安全的
    # 保持单个链接对象是可以开通多个频道与之通信
    @property
    def get_channel(self):
        if self.channel is None or self.channel.is_closed:
            if self.connection.is_closed:
                Lock.acquire()
                self.connection = self.connect()
                channel = self.connection.channel()
                Lock.release()
                # 声明每次只获取一条消息
                channel.basic_qos(prefetch_count=1)
                # 声明队列永久化
                channel.queue_declare(self.queue_name, durable=True)
                self.channel = channel
        return self.channel

    # 从rabbitmq队列中获取一条消息
    # 消息都是经过pickle序列化的
    def get(self):
        channel = self.get_channel
        method, properties, body = channel.basic_get(self.queue_name)
        body = pickle.loads(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return body

    # 队列中是否为空
    @property
    def is_empty(self):
        channel = self.get_channel
        method, properties, body = channel.basic_get(self.queue_name)
        if not all((method, properties, body)):
            return True
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag)
            return False

    # 向队列中发布消息
    def put(self, body, exchange=''):
        body = pickle.dumps(body)
        channel = self.get_channel
        channel.basic_publish(exchange=exchange, routing_key=self.queue_name,
                                body=body, proeprties=pika.BasicProperties(delivery_mode=2))
        
    def close(self):
        channel = self.get_channel
        channel.close()

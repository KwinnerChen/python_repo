#! usr/bin/env python3
# -*- coding: utf-8 -*-


from time import sleep
from threading import Thread, current_thread, RLock
import logging
import random
import pika
import abc


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
shand = logging.StreamHandler()
sformat = logging.Formatter('%(message)s')
shand.setFormatter(sformat)
logger.addHandler(shand)


_LOCK = RLock()


class RabbitBasic(abc.ABC):
    """
    
    """

    __connection = None  # 每个进程中只有一个链接实例

    def __new__(cls, host='192.168.3.30', port=5672, vh='/', username='admin', password='880326'):
        
        cls.host = host
        cls.port = port
        cls.vh = vh
        cls.username = username
        cls.password = password
        cls._cred = pika.PlainCredentials(cls.username, cls.password)
        cls._con_params = pika.ConnectionParameters(host=cls.host, port=cls.port, virtual_host=cls.vh, credentials=cls._cred)
        return object.__new__(cls)

    def __init__(self):
        self.__channel = None

    @classmethod
    def __connect_mq(cls):
        if cls.__connection is None or not cls.__connection.is_open:
            cls.__connection = pika.BlockingConnection(cls._con_params)
        return cls.__connection

    @classmethod
    def __reconnect(cls):
        cls.__connection = cls.__connect_mq()

    @classmethod
    def get_connection(cls):
        """
        获取链接实例，没有或者断开则重建
        """
        if cls.__connection is None or not cls.__connection.is_open:
            cls.__reconnect()
        return cls.__connection

    def get_channel(self):
        """
        获取通道实例，没有或者断开重建
        """
        if self.__connection is None or not self.__connection.is_open:
            self.__reconnect()
            self.__channel = self.__connection.channel()
        elif self.__channel is None or not self.__channel.is_open:
            self.__channel = self.__connection.channel()             
        return self.__channel

    def declare(self, queue,
                      passive=False,
                      durable=False,
                      exclusive=False,
                      auto_delete=False,
                      arguments=None
                      ):
        """
        声明一个队列
        """
        channel = self.get_channel()
        channel.queue_declare(queue=queue,
                      passive=passive,
                      durable=durable,
                      exclusive=exclusive,
                      auto_delete=auto_delete,
                      arguments=arguments
                      )

    def queue_bind(self,
                   queue,
                   exchange,
                   routing_key=None,
                   arguments=None
                   ):
        """
        绑定一个队列到指定交换机
        """
        channel = self.get_channel()
        channel.queue_bind(queue=queue,
                   exchange=exchange,
                   routing_key=routing_key,
                   arguments=arguments
                   )

    def basic_qos(self,
                  prefetch_size=0,
                  prefetch_count=0,
                  global_qos=False
                  ):
        """
        指定队列行为，如每次获取队列信息条数等
        """
        channel = self.get_channel()
        channel.basic_qos(prefetch_size=prefetch_size,
                          prefetch_count=prefetch_count,
                          global_qos=False
                          )

    def close(self):
        channel = self.get_channel()
        channel.close()
        connection = self.get_connection()
        connection.close()


class RabbitPublic(RabbitBasic):
    def publish(self, exchange,
                      routing_key,
                      body,
                      properties=None,
                      mandatory=False):
        channel = self.get_channel()
        channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=body,
                      properties=properties,
                      mandatory=mandatory)


class RabbitConsumer(RabbitBasic):
    def consume(self, queue,
                      on_message_callback,
                      auto_ack=False,
                      exclusive=False,
                      consumer_tag=None,
                      arguments=None
                      ):
        """
        只针对单线程
        """
        channel = self.get_channel()
        self.basic_qos(prefetch_count=1)  # 声明负载均衡
        channel.basic_consume(queue=queue,
                      on_message_callback=on_message_callback,
                      auto_ack=auto_ack,
                      exclusive=exclusive,
                      consumer_tag=consumer_tag,
                      arguments=arguments
                      )
        channel.start_consuming()

    def consume_multithread(self, queue, callback):
        """
        多线程消费队列
        """
        _LOCK.acquire()
        channel = self.get_channel()
        self.basic_qos(prefetch_count=1)
        _LOCK.release()
        while True:
            _LOCK.acquire()
            message = channel.basic_get(queue)
            _LOCK.release()
            if message[-1] is None:
                break
            result = callback(message[-1])
            _LOCK.acquire()
            channel.basic_ack(delivery_tag=message[0].delivery_tag)
            _LOCK.release()


def push_message(queue, message, count=1):
    r = RabbitPublic()
    for i in range(count):
        r.publish(exchange='', routing_key=queue, body=message)


def consume_mutlthread(queue, callback, thread_num):
    tl = []
    for i in range(thread_num):
        r = RabbitConsumer()
        t = Thread(target=r.consume_multithread, args=(queue, callback))
        t.start()
        tl.append(t)
    for t in tl:
        t.join()


def callback(ch, method, properties, body):
    logger.info('%s print %s' % (current_thread().name, body))
    logger.info('ch: %s' % ch)
    logger.info('method: %s' % method)
    logger.info('properties: %s' % properties)
    sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback_multithread(message):
    logger.info('%s print %s' % (current_thread().name, message))
    sleep(2)


if __name__ == '__main__':
    #push_message('test', 'hello', 200)
    
    consume_mutlthread('test', callback_multithread, 50)
       
    

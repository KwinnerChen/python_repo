#! usr/bin/env python3
# -*- coding: utf-8 -*-


# 放弃这种方法
# 见rabbitmq_multithread_test.py


from time import sleep
import logging
import random

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
shand = logging.StreamHandler()
sformat = logging.Formatter('%(message)s')
shand.setFormatter(sformat)
logger.addHandler(shand)


###################################################################################################


import pika
import abc
from threading import Thread, current_thread, RLock


class Connection(abc.ABC):
    def __init__(self, host='192.168.3.30', port=5672, vh='/', username='admin', password='880326'):
        self.host = host
        self.port = port
        self.vh = vh
        self.username = username
        self.passwrod = password
        self._cred = pika.PlainCredentials(self.username, self.passwrod)
        self._con_params = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vh, credentials=self._cred)
        self._connection = None

    def __connect_mq(self):
        self._connection = pika.BlockingConnection(self._con_params)
        return self._connection

    def __reconnect(self):
        self._connection = self.__connect_mq()
        return self._connection

    def get_connection(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = self.__reconnect()
        return self._connection


class RabbitBasic(abc.ABC):
    """
    一个rabbitmq链接对象的基类，在一个进程中值允许有一个链接实例connection，而在此链接实例上可以允许多个
    通道channel实例，获取多个通道实例只需要实例多个基类。
    """
    # lock = RLock()

    # lock.acquire()
    # __connection = None  # 每个进程中只有一个链接实例
    # lock.release()

    # def __new__(cls, host='192.168.3.30', port=5672, vh='/', username='admin', password='880326'):
    #     cls.host = host
    #     cls.port = port
    #     cls.vh = vh
    #     cls.username = username
    #     cls.password = password
    #     cls._cred = pika.PlainCredentials(cls.username, cls.password)
    #     cls._con_params = pika.ConnectionParameters(host=cls.host, port=cls.port, virtual_host=cls.vh, credentials=cls._cred)
    #     return object.__new__(cls)

    def __init__(self, connection):
        self.__connect_class = connection
        self.__connection = None
        self.__channel = None

    # @classmethod
    # def __connect_mq(cls):
    #     if cls.__connection is None or not cls.__connection.is_open:
    #         cls.__connection = pika.BlockingConnection(cls._con_params)
    #     return cls.__connection

    # @classmethod
    # def __reconnect(cls):
    #     cls.__connection = cls.__connect_mq()

    # def get_connection(self):
    #     """
    #     获取链接实例，没有或者断开则重建
    #     """
    #     if not self.__connection.is_open:
    #         cls.__reconnect()
    #     return cls.__connection

    def get_channel(self):
        """
        获取通道实例，没有或者断开重建
        """
        if self.__connection is None or self.__connection.is_closed:
            self.__connection = self.__connect_class.get_connection()
            self.__channel = self.__connection.channel()
        elif self.__channel is None or self.__channel.is_closed:
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

    # def close(self):
    #     channel = self.get_channel()
    #     channel.close()
    #     connection = self.get_connection()
    #     connection.close()


class RabbitPublic(RabbitBasic):
    def publish(self, exchange,
                      routing_key,
                      body,
                      properties=None,
                      mandatory=False):
        channel = self.get_channel()
        self.declare('test', durable=True)
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
        channel = self.get_channel()
        self.declare('test', durable=True)
        self.basic_qos(prefetch_count=1)  # 声明负载均衡
        channel.basic_consume(queue=queue,
                      on_message_callback=on_message_callback,
                      auto_ack=auto_ack,
                      exclusive=exclusive,
                      consumer_tag=consumer_tag,
                      arguments=arguments
                      )
        channel.start_consuming()


def push_message(connection, queue, message, count=1):
    r = RabbitPublic(connection)
    for i in range(count):
        r.publish(exchange='', routing_key=queue, body=message)


def consume_mutlthread(connection, queue, callback, thread_num):
    tl = []
    for i in range(thread_num):
        r = RabbitConsumer(connection)
        # logger.info('%d' % id(r.get_connection()))
        t = Thread(target=r.consume, args=(queue, callback))
        t.start()
        tl.append(t)
        sleep(1)
    for t in tl:
        t.join()


def callback(ch, method, properties, body):
    logger.info('%s print %s' % (current_thread().name, body))
    logger.info('ch: %s' % ch)
    logger.info('method: %s' % method)
    logger.info('properties: %s' % properties)
    sleep(random.random() * 2)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = Connection()
    # push_message(connection, 'test', 'hello', 200)
    consume_mutlthread(connection, 'test', callback, 5)
       
    

#! /usr/bin python3
# -*- coding: utf-8 -*-


import pika
from threading import Thread, current_thread
from time import sleep
from random import random
import logging


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
shand = logging.StreamHandler()
sformat = logging.Formatter('%(message)s')
shand.setFormatter(sformat)
logger.addHandler(shand)


class Connection():
    def __init__(self, host='192.168.3.30', port=5672, vh='/', username='admin', password='880326'):
        self.host = host
        self.port = port
        self.vh = vh
        self.username = username
        self.passwrod = password
        self._cred = pika.PlainCredentials(self.username, self.passwrod)
        self._con_params = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vh, credentials=self._cred)
        self._connection = None
        self._channel = None

    def __connect_mq(self):
        self._connection = pika.BlockingConnection(self._con_params)
        return self._connection

    def __reconnect(self):
        self._connection = self.__connect_mq()
        return self._connection

    def get_connection(self):
        if self._connection is None or not self._connection.is_open:
            self._connection = self.__reconnect()
        return self._connection


def worker_func(connection, callback):
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume('test', callback)
    channel.start_consuming()


def callback(ch, method, properties, body):
    logger.info('%s print %s' % (current_thread().name, body))
    logger.info('ch: %s' % ch)
    logger.info('method: %s' % method)
    logger.info('properties: %s' % properties)
    sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_multithreading(connection, callback, thread_num):
    thread_list = []
    for i in range(thread_num):
        t = Thread(target=worker_func, args=(connection, callback))
        t.start()
        thread_list.append(t)
        sleep(random())
    for t in thread_list:
        t.join()


def test():
    def create_channel(connection):
        channel = connection.channel()
        channel.queue_declare('test', durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume('test', callback)
        channel.start_consuming()
    con = Connection()
    connection = con.get_connection()
    print(connection)
    for i in range(5):
        Thread(target=create_channel, args=(connection,)).start()
        sleep(1)
    sleep(20)


if __name__ == '__main__':
    # connection = Connection().get_connection()
    # run_multithreading(connection, callback, 3)
    test()
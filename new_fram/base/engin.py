#! usr/bin/env python3
# -*- coding: utf-8 -*-
# TODO:基本框架，细节还需完善


__author__ = "Kwinner Chen"


import config
from time import sleep
from base import Task, Item
from threading import Thread
from storageconf import StorageType


class Engin:
    def __init__(self, downloader, storage, q_task, q_result, q_storage, logger):
        self.downloader = downloader
        # self.spider = spider
        self.storage = storage
        self.q_task = q_task
        self.q_result = q_result
        self.q_storage = q_storage
        self.logger = logger
        self.thread_list = []

    def __do_download(self):
        while True:
            task = self.__get_task(self.q_task)
            if task == 1:
                sleep(1)
                continue
            elif task == 2:
                break
            else:
                try:
                    _task, errmess = self.downloader.get_page(task)
                    if not errmess:
                        self.q_result.put(_task)
                    else:
                        if _task.times > config.TIMES:
                            self.logger.warning('%s <%s>' % (_task, errmess))
                except AssertionError as e:
                    self.logger.warning('%s <%s>' % (_task, e))
            del task
        
    def __do_parse(self):
        while True:
            task = self.__get_task(self.q_result)
            if task == 1:
                sleep(1)
                continue
            elif task == 2:
                break
            else:
                try:
                    r = self.__do_callback(task)
                    if isinstance(r, Task):
                        self.q_task.put(r)
                    elif isinstance(r, Item):
                        self.q_storage.put(r)
                    del task
                except Exception as e:
                    self.logger.warning('%s解析失败[%s]' % (task, e))
            del task

    def __get_task(self, q_):
        if q_.empty():
            r = 1
        else:
            task = q_.get()
            if task is None:
                r = 2
            else:
                r = task
        return r

    def __do_storage(self, q_storage):
        while True:
            item = self.__get_task(q_storage)
            if item == 1:
                sleep(1)
                continue
            elif item == 2:
                break
            else:
                try:
                    if config.STORAGE_TYPE == StorageType.Json:
                        from threading import RLock
                        lock = RLock()
                        r = self.storage.save(item, lock)
                    else:
                        r = self.storage.save(item)
                    self.logger.info(r)
                except Exception as e:
                    self.logger.warning('%s <%s>' % (item, e))
        
    def __do_callback(self, task):
        response = task.response
        callback = task.callback
        return callback(response)

    def __main(self, t_thread_num=1, r_thread_num=1, s_thread_num=1):
        for i in range(t_thread_num):
            t_t = Thread(target=self.__do_download, name='download_thread_%d' % i) 
            self.thread_list.append(t_t)
            t_t.start()

        for j in range(r_thread_num):
            r_t = Thread(target=self.__do_parse, name='parser_thread_%d' % j)
            self.thread_list.append(r_t)
            r_t.start()

        for k in range(s_thread_num):
            s_t = Thread(target=self.__do_storage, name='storage_thread_%d' % k)
            self.thread_list.append(s_t)
            s_t.start()

    def run(self, t_thread_num=1, r_thread_num=1, s_thread_num=1):
        self.t_thread_num = t_thread_num
        self.r_thread_num = r_thread_num
        self.s_thread_num = s_thread_num
        self.__main(t_thread_num=1, r_thread_num=1, s_thread_num=1)

    def stop(self):
        self.__clear_t_queue()

        for i in range(self.t_thread_num):
            self.q_task.put(None)
        
        for t in self.thread_list:
            if 'dowload' in t.name:
                t.join()

        for i in range(self.r_thread_num):
            self.q_result.put(None)

        self.logger.info('等待解析列队中剩余任务完成.......')
        for t in self.thread_list:
            if 'parser' in t.name:
                t.join()

        for i in range(self.s_thread_num):
            self.q_storage.put(None)

        self.logger.info('等待存储列队中剩余任务完成........')
        for t in self.thread_list:
            if 'storage' in t.name:
                t.join()

        del self.thread_list[:]  # 清空线程列表

    def __clear_t_queue(self):
        while not self.q_task.empty():
            task = self.q_task.get()
            del task


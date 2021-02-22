#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from .configmodul import Config
from importlib import import_module


def get_storager():
    if getattr(Config, 'STORAGE_MODUL', None):
        modul_list = Config.STORAGE_MODUL.value.split('.')
        name = modul_list[-1]
        package = '.'.join(modul_list[:-1])
        storager_module = import_module(package)
        Storager = getattr(storager_module, name)
        return Storager(Config.STORAGE_CONFIG)
    else:
        raise AttributeError("%s 声明的对象并未定义!" % name)


def get_queue(queue_name):
    if getattr(Config, 'QUEUE_MODUL', None):
        modul_list = Config.QUEUE_MODUL.value.split('.')
        name = modul_list[-1]
        package = '.'.join(modul_list[:-1])
        queue_modul = import_module(package)
        Queue = getattr(queue_modul, name)
        return Queue(Config.QUEUE_CONFIG, queue_name)
    else:
        raise AttributeError("%s 声明的对象并未定义!" % name)

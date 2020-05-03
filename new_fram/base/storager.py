#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from base.configmodul import Config


def get_storager():
    if Config.STORAGE_MODUL.value:
        from importlib import import_module
        modul_list = Config.STORAGE_MODUL.value.split('.')
        name = modul_list[-1]
        package = '.'.join(modul_list[:-1])
        storager_module = import_module(package)
        Storager = getattr(storager_module, name)
        return Storager(Config.STORAGE_CONFIG)
    else:
        raise AttributeError("%s 声明的对象并未定义1")


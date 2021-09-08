#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from models import Field
from typing import Iterable


class ArgumentError(Exception):
    pass


class ItemMeta(type):
    def __new__(cls, name, bases, attr_dict):
        for k, v in attr_dict.items():
            if isinstance(v, Field):
                v.storage_name = '__{}'.format(k)
            elif not k.startswith('_') and isinstance(v, (str, float, int, Iterable)):
                raise ValueError(f"{k}的定义必须是一个Field类的实例")
        return type.__new__(cls, name, bases, attr_dict)


class ItemBase(metaclass=ItemMeta):
    def __init__(self, *args, **kwargs):
        cls = self.__class__
        for arg in args:
            if isinstance(arg, dict):
                kwargs.update(arg)
            else:
                raise ArgumentError(f"{arg}应该是一个字典")
        for k, v in kwargs.items():
            if k in cls.__dict__:
                setattr(self, k, v)  # 设置实例话参数，又描述符接管
            else:
                raise ValueError("%s 并未定义，并且必须定义为类变量！" % k)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __iter__(self):
        cls = self.__class__
        for k, v in cls.__dict__.items():
            if isinstance(v, Field):
                value = getattr(self, k)
                yield k, value

    def __len__(self):
        return len(tuple(self.keys()))

    def __str__(self):
        return str(dict(self))

    def keys(self):
        cls = self.__class__
        for k, v in cls.__dict__.items():
            if isinstance(v, Field):
                yield k

    def values(self):
        cls = self.__class__
        for k, v in cls.__dict__.items():
            if isinstance(v, Field):
                yield getattr(self, k)

    def items(self):
        return self.__iter__()
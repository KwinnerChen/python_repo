#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import abc
from datetime import datetime


class BaseField:
    def __init__(self):
        self.storage_name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if getattr(instance, self.storage_name, None):
            raise KeyError("%s 已被赋值，不可更改！" % self.storage_name.strip('_'))
        setattr(instance, self.storage_name, value)

    def __str__(self):
        return self.__class__.__name__


class Field(abc.ABC, BaseField):
    def __set__(self, instance, value):
        self.validate(value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, value):
        """检查值类型是否正确"""


def validate(value, storage_name, type_str: str):
    if type(value).__name__ != type_str:
        raise ValueError("%s 实际存储值 %s 并非定义中的 %s 类型！" % (storage_name.strip('_'), value, type_str))


class StrField(Field):
    def validate(self, value):
        validate(value, self.storage_name, 'str')
        # if type(value).__name__ != 'str':
        #     raise ValueError("%s 实际存储值 %s 并非定义中的 %s 类型！" % (self.storage_name.strip('_'), value, "str"))
        

class IntField(Field):
    def validate(self, value):
        validate(value, self.storage_name, 'int')
        # if type(value).__name__ != 'int':
        #     raise ValueError("%s 实际存储值 %s 并非定义中的 %s 类型！" % (self.storage_name.strip('_'), value, "int"))


class FloatField(Field):
    def validate(self, value):
        validate(value, self.storage_name, 'float')
        # if type(value).__name__ != 'float':
        #     raise ValueError("%s 实际存储值 %s 并非定义中的 %s 类型！" % (self.storage_name.strip('_'), value, "float"))


class DateTimeField(Field):
    def validate(self, value):
        validate(value, self.storage_name, 'datetime')
        # if not isinstance(value, datetime):
        #     raise ValueError("%s 实际存储值 %s 并非定义中的 %s 类型！" % (self.storage_name.strip('_'), value, "datetime"))
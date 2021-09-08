#! /usr/bin/env python3
# -*- coding: utf-8 -*-


try:
    import config
except ImportError:
    pass
import configglobal


# ConfigValue = namedtuple("ConfigValue", "name value")


class ConfigMeta(type):
    """配置类对象的元类，用于将配置文件解析到类对象"""
    @classmethod
    def __prepare__(cls, name, bases):  # 3个位置参数是必须的
        attrs = {k: v for k, v in configglobal.__dict__.items() if k.isupper() and not k.startswith('_')}
        if "config" in globals():
            for k, v in config.__dict__.items():
                if not k.startswith('_') and k.isupper():
                    attrs[k] = v
        return attrs

    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            raise Exception("不可对属性重新赋值")
        super().__setattr__(name, value)

    def __dir__(cls):
        return [k for k in cls.__dict__.keys() if k.isupper() and not k.startswith('_')]


class Config(metaclass=ConfigMeta):
    """配置类对象，配置参数为类属性，不可实例化"""
    def __new__(cls):
        raise Exception("配置类不可实例化")
    
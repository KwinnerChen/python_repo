#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
一个描述符类的定义，也是面向对象，类编程的一个范例
"""


import abc


# 创建一个描述符类
class AutoStorage:
    __counter = 0                                           # 初始化一个简单计数器，计数器不是必须的，可以定义实例话时的参数

    def __init__(self):
        cls = self.__class__                                # 实例内省，返回实例的直接类
        prefix = cls.__name__                               # 类内省，返回类名
        index = cls.__counter                               # 获取类变量，使其在实例内可赋值
        self.storage_name = '_{}#{}'.format(prefix, index)  # 实例属性，每个实例值不同
        cls.__counter += 1                                  # 操作类变量

    def __get__(self, instance, owner):
        # 定义描述符基本操作
        # 具有__get__, __set__, __delete__即为描述符
        # 把一个类实例变量托管到一个描述符实例上
        # 针对该实例变量的读取，赋值，删除操作都通过描述符实现
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name )

    def __set__(self, instance, value):
        # 对描述符接管的变量的赋值经过该方法
        setattr(instance, self.storage_name, value)


# 定义一个描述符基类
class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """返回一个验证过的值，或者抛出错误"""


class Quantity(Validated):
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('Value must be > 0.')
        return value


class NonBlank(Validated):
    def validate(self, instance, value):
        if len(value.strip()) == 0:
            raise ValueError('Value cannot be empty or blanc.')
        return value


def entity(cls):
    # 一个类装饰器，可以自动给托管变量取名
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Validated):  # 是否是一个描述符实例
            # 猴子补丁
            attr.storage_name = '_{}#{}'.format(attr.__class__.__name__, key)
            print(attr.storage_name)
    return cls

#########################################################################
# 或者使用闭包实现描述符
def quantity(storage_name):
    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value <= 0:
            raise ValueError('Value must be > 0')
        return setattr(instance, storage_name, value)

    return property(qty_getter, qty_setter)  # 利用了property装饰器


# 没有使用参数的版本
def quantity_():
    try:
        quantity.counter += 1  # python中函数也是一等对象，自然可以访问其属性的方式访问内部变量
    except AttributeError:
        quantity.counter = 0
    storage_name = '_{}#{}'.format('quantity', quantity.counter)
    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value <= 0:
            raise ValueError('Value must be > 0')
        setattr(instance, storage_name, value)

    return property(qty_getter, qty_setter)  # 利用了property装饰器

    
# 装饰器的提示
# class A:
#     def __init__(self, some):
#         self.some = some
#     @property
#     def some(self):
#         return self.__dict__['some']
#     @some.setter
#     def some(self, value):
#         self.__dict__['some'] = value
# 或者
# class A:
#     def __init__(self, some):
#         self.some = some
#     def get_some(self):
#         return self.__dict__['some']
#     def set_some(self, value):
#         self.__dict__['some'] = value
#     some = property(get_some, set_some)  # 这是一个类变量，只是没有定义在开头



##########################################################################


# 一个使用描述符类的示例
@entity
class LineItem:
    # 定义描述符，在类变量中
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    # def __new__(cls, description, weight, price):  # __new__方法可以指定自动指定名称，但是代码复用太低，可以使用类装饰器或者元类
    #     cls.weight.storage_name = '_Quantity#weight'
    #     return object.__new__(cls)

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    i = LineItem('watch', 10, 12)
    print(i.weight)
    print(getattr(i, '_Quantity#weight'))
    
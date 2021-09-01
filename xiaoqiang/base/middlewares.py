# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod
from base.task import Task


class MiddleWare(ABC):
    """
    请求任务中间件的基类，自定义中间件需继承自该类。对请求任务发出钱做一些预处理。
    比如使用IP代理等。
    """
    
    def process(self, task):
        """
        参数必须是Task对象，且最终返回值也必须是Task对象。
        """
        assert isinstance(task, Task), f"请求中间件{self.__class__.__name__}只能接受任务对象为参数！"
        task = self.task_process(task)
        assert isinstance(task, Task) or task is None, f"请求中间件{self.__class__.__name__}只能返回一个任务对象或者None！"
        return task

    @abstractmethod
    def task_process(self, task):
        """
        参数为Task对象，返回值也必须时Task对象。
        """
        return task
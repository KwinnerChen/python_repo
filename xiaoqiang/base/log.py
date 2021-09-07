#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Kwinner Chen'


from base.utils import import_module
from logging.handlers import TimedRotatingFileHandler
import logging
import os.path
from os import mkdir
from configmodul import Config


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR


class Logger(object):
    """
        用于日志记录！每日一个日志文件。多线程可用，多进程会造成日志文件混乱丢失。
    """

    def __init__(self, logfile_name: str, logger_name=__name__) -> None:
        """
        初始化一个日志记录器。线程安全，多进程时应考虑日志文件是否会混乱。notifier是一个用于事件提醒的类或者该类的实例，
        提醒等级notify_level默认为logging.WARNING。当使用方法高于该等级时会进行事件通知。
        记录器默认等级为DEBUG，可以将配置文件的DEBUG字段改为False来设置为INFO。
        :params:
        :logfile_name: str, 日志文件名，线程安全。但是多进程时考虑文件会混乱。
        :logger_name: str, 记录器名称。同logging模块中的Logger。以当前模块名称命名。
        """
        self.logger = logging.getLogger(logger_name)
        if Config.DEBUG:
            self.logger.setLevel(DEBUG)
        else:
            self.logger.setLevel(INFO)

        logfile_name = os.path.join(Config.LOG_FILE_PATH, logfile_name)
        if not os.path.exists(Config.LOG_FILE_PATH):
            mkdir(Config.LOG_FILE_PATH)

        if not self.logger.hasHandlers():
            self.__init_a_logger(logfile_name)
        
        notifier = import_module(Config.NOTIFIER)
        if callable(notifier):
            notifier = notifier(**Config.NOTIFIER_CONFIG)
        self.notifier = notifier

    def __init_a_logger(self, logfile_name) -> None:
        """
        初始化一个日志记录器，文件名为logfile_name。日志文件每天轮替，保存30的文件。
        终端输出等级为DEBUG，文件输出等级为WARNING。
        """
        sh = logging.StreamHandler()
        sh.setLevel(DEBUG)
        fh = TimedRotatingFileHandler(filename=logfile_name, when="D", backupCount=30)
        fh.setLevel(WARNING)
        fmt_fh = logging.Formatter(r"%(actime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
        fmt_sh = logging.Formatter(r"%(actime)s - %(levelname)s - %(message)s")
        sh.setFormatter(fmt_sh)
        fh.setFormatter(fmt_fh)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def __notify(self, msg):
        try:
            senderr = self.notifer.notify(msg)
        except Exception as e:
            self.logger.error(f"事件通知发生错误，错误原因: {e}")
        else:
            self.logger.warning(f"事件通知可能部分错误，错误原因：{senderr}")

    def info(self, msg: str, notify=False) -> None:
        self.logger.info(msg)
        if self.notifer and notify:
            self.__notify(msg)

    def debug(self, msg: str, notify=False) -> None:
        self.logger.debug(msg)
        if self.notifer and notify:
            self.__notify(msg)

    def warning(self, msg: str, notify=True) -> None:
        self.logger.warning(msg)
        if self.notifer and notify:
            self.__notify(msg)

    def error(self, msg: str, notify=True) -> None:
        self.logger.error(msg)
        if self.notifer and notify:
            self.__notify(msg)

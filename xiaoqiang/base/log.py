#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Kwinner Chen'


from logging.handlers import TimedRotatingFileHandler
import logging
import os.path
from os import mkdir


__log_file_path = os.path.join(os.getcwd(), 'log')


class Logger(object):
    """
        用于日志记录！每日一个日志文件。多线程可用，多进程会造成日志文件混乱丢失。
    """
    logger = logging.getLogger(__file__)

    def __init__(self, logfile_name: str) -> None:
        logfile_name = os.path.join(__log_file_path, logfile_name)
        if not os.path.exists(__log_file_path):
            mkdir(__log_file_path)
        if not self.logger.hasHandlers():
            self.__init_a_logger(logfile_name)

    def __init_a_logger(cls, logfile_name) -> None:
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        fh = TimedRotatingFileHandler(filename=logfile_name, when="D", backupCount=30)
        fh.setLevel(logging.WARNING)
        fmt_fh = logging.Formatter(r"%(actime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
        fmt_sh = logging.Formatter(r"%(actime)s - %(levelname)s - %(message)s")
        sh.setFormatter(fmt_sh)
        fh.setFormatter(fmt_fh)
        cls.logger.addHandler(sh)
        cls.logger.addHandler(fh)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def set_log_level(self, level: logging._Levle) -> None:
        self.logger.setLevel(level)
#! usr/bin/env python3
# -*- coding: utf-8 -*-
# TODO:大致框架，细节还需完善


__author__ = 'Kwinner Chen'


import logging
import os
import re
from datetime import datetime


_file_path = os.path.join(os.getcwd(), 'log')


class Logger(object):
    """
        用于日志记录！每日一个日志文件。
    """

    def __init__(self):
        self.__trytomkdir()
        self.filename = self.__get_filename()
        self.logger = self.__logger_gener()

    def __trytomkdir(self):
        if not os.path.exists(_file_path):
            os.mkdir(_file_path)        

    def __logger_gener(self):
        logger = logging.getLogger()
        self.fh = logging.FileHandler(self.filename)
        sh = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
        self.fh.setLevel(logging.WARNING)
        sh.setLevel(logging.INFO)
        fm = logging.Formatter('%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
        self.fh.setFormatter(fm)
        sh.setFormatter(fm)
        logger.addHandler(self.fh)
        logger.addHandler(sh)
        return logger

    def info(self, mess):
        self.__update_filename()
        self.logger.info(mess)
        pass

    def debug(self, mess):
        self.__update_filename()
        self.logger.debug(mess)
        pass

    def warning(self, mess):
        self.__update_filename()
        self.logger.warning(mess)
        pass

    def erro(self, mess):
        self.__update_filename()
        self.logger.error(mess)
        pass

    def __check_filename(self):
        last_file = self.__get_lastfile()
        if last_file:
            lasttime = re.search(r'log-(\d{6})\.log', last_file)
            lasttime = lasttime.group(1) if lasttime else None
            if lasttime < datetime.now().strftime('%y%m%d'):
                return False
            else:
                return True
        else:
            return False

    def __get_lastfile(self):
        file_list = [i.name for i in os.scandir(_file_path)]
        if not file_list:
            return None
        else:
            file_list.sort(reverse=True)
            last_file = file_list[0] if file_list else ''
            return last_file

    def __update_filename(self):
        if not self.__check_filename():
            self.filename = self.__get_filename()
            self.logger.removeFilter(self.fh)
            self.fh = logging.FileHandler(self.filename)
            self.fh.setLevel(logging.WARNING)
            fm = logging.Formatter('%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
            self.fh.setFormatter(fm)
            self.logger.addHandler(self.fh)

    def __get_filename(self):
        return os.path.join(_file_path, 'log-%s.log' % datetime.now().strftime('%y%m%d'))
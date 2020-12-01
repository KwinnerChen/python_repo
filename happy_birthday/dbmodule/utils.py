# -*- coding: utf-8 -*-


from enum import Enum


class DBType(Enum):
    Mysql = "pymysql"
    Oracle = "cx_Oracle"
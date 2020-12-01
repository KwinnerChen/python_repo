# -*- coding: utf-8 -*-


from DBUtils.PersistentDB import PersistentDB
from .utils import DBType
from importlib import import_module
import config


__all__ = ["get_a_dbpool"]


# alert_str = """必须在config文件中完善数据库的配置信息
#                 DB = {
#                     "db_type": str,
#                     "db_name": str,
#                     "host": str,
#                     "port": int,
#                     "user": str,
#                     "password": str,
#                     }
#             """
# assert hasattr(config, 'DB'), alert_str


def __get_dbname():
    return config.DB['db_name']


def __get_dbtype():
    return config.DB['db_type']


def __get_port():
    return config.DB['port']


def __get_host():
    return config.DB['host']


def __get_user():
    return config.DB['user']


def __get_password():
    return config.DB['password']


def get_a_dbpool(maxusage=None, setsession=None, failures=None, ping=1,
            closeable=False, threadlocal=None):
    db_type = __get_dbtype()
    kw = {
        'db': __get_dbname(),
        'host': __get_host(),
        'port': __get_port(),
        'user': __get_user(),
        'password': __get_password()
    }
    
    if db_type == DBType.Mysql:
        creater = import_module(DBType.Mysql.value)
    elif db_type == DBType.Oracle:
        creater = import_module(DBType.Oracle.value)
    
    return PersistentDB(creater, maxusage=None, setsession=None, failures=None, ping=1,
            closeable=False, threadlocal=None, **kw)

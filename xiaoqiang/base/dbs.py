#! usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Kwinner Chen'


import os
import abc
from base.item import ItemBase
from threading import RLock
try:
    from dbutils.pooled_db import PooledDB
except ImportError:
    from DBUtils.PooledDB import PooledDB


class DBBase(abc.ABC):
    DBPOOL = None

    def __new__(cls, config):
        if cls.__name__ == 'Mysql':
            import pymysql as creator
        elif cls.__name__ == 'Oracle':
            import cx_Oracle as creator

        if not cls.DBPOOL:
            cls.DBPOOL = PooledDB(creator, maxconnections=config.THREAD_NUM, **config.STORAGE_CONFIG)

        return super().__new__(cls)

    def __init__(self, config):
        self.config = config
        for k, v in config.STORAGE_CONFIG.items():
            setattr(self, k, v)
 
    def save(self, item, tablename):
        con = self.DBPOOL.connection()
        cur = con.cursor()
        r = 0
        try:
            if isinstance(item, (ItemBase, dict)):
                r = self.saveone(cur, item, tablename)
            elif isinstance(item, (list, tuple)):
                r = self.savemany(cur, item, tablename)
            con.commit()
        finally:
            cur.close()
            con.close()
        return r

    @abc.abstractmethod
    def saveone(self, cur, item, tablename):
        return 0

    @abc.abstractmethod
    def savemany(self, cur, item, tablename):
        return 0

    @classmethod
    def close(cls):
        """该方法只是显示关闭池中现有链接，如果再次使用存储的化仍旧会自动创建
        链接。"""
        cls.DBPOOL.close()

    def __del__(self):
        """销毁对象是关闭链接"""
        try:
            self.close()
        except:
            pass
    

class Mysql(DBBase):
    def saveone(self, cur, item, tablename):
        sql = '''
        insert into
        {tablename}({field})
        values({value})
        '''
        sql = sql.format(tablename=tablename, field=','.join(item.keys()), value=','.join(('%s',)*len(item)))
        r = cur.execute(sql, tuple(item.values()))
        return r

    def savemany(self, cur, item, tablename):
        sql = '''
        insert into 
        {tablename}({field}) 
        values({value})
        '''
        sql = sql.format(tablename=tablename, field=','.join(item[0].keys()), value=','.join(('%s',)*len(item[0])))
        r = cur.executemany(sql, (tuple(i.values()) for i in item))
        return r

            
class Oracle(DBBase):
    def saveone(self, cur, item, tablename):
        sql = '''
        insert into 
        {tablename}({field}) 
        values({value})
        '''
        sql = sql.format(tablename=tablename, field=','.join(item.keys()), value=':'.join(item.keys()))
        r = cur.execute(sql, item)
        return r

    def savemany(self, cur, item, tablename):
        sql = '''
        insert into 
        {tablename}({field}) 
        values({value})
        '''
        sql = sql.format(tablename=tablename, field=','.join(item[0].keys()), value=':'.join(item[0].keys()))
        r = cur.executemany(sql, item)
        return r


# class Local:
#     __lock = RLock()

#     def __init__(self, storageconf):
#         self.__count = 1
#         for k, v in storageconf.value.items():
#             setattr(self, k, v)
#         # self.type = storageconf.value['type']
#         self.__check_path()

#     def __valid_filename(self, filename):
#         if not filename:
#             return self.filename
#         if not filename.endswith('.txt'):
#             filename += '.txt'
#             return filename

#     def __check_filesize(self, filename):
#         if not os.path.exists(os.path.join(self.file_path, filename)):
#             return filename
#         if os.path.getsize(os.path.join(self.file_path, filename))>104857600:
#             filename = filename.splie('.')[0] + self.__count
#             self.__count += 1
#             return filename + '.txt'
#         else:
#             return filename

#     def __check_path(self):
#         try:
#             os.makedirs(self.file_path)
#         except IOError:
#             pass

#     def save(self, item, filename=None):
#         filename = self.__check_filesize(self.__valid_filename(filename))
#         self.filename = filename
#         count = 0
#         self.__lock.acquire()
#         try:
#             with open(os.path.join(self.file_path, self.filename), mode=self.mode, encoding=self.encoding) as f:
#                 if isinstance(item, ItemBase):
#                     f.write(str(item)+'\n')
#                     count += 1
#                 elif isinstance(item, (list, tuple)):
#                     for i in item:
#                         f.write(str(i) + '\n')
#                         count += 1
#         finally:
#             self.__lock.release()

#         return count

#     def close(self):
#         # 此方法只是为了和数据库接口统一
#         pass

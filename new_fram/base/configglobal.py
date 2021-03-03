"""全局配置参数，所有可配置参数都列在这里。字段被解析为Config类对象，每个字段对应一个类属性，
   属性值为字段值。根目录下可以有单独配置文件，文件中列出的字段将覆盖默认字段。
"""

import os

# 线程数
THREAD_NUM = 1

# 下载任务重试次数
RETRY_TIMES = 0

# 此变量为了将来可扩展自定义数据库存储模块
# 注册自定存储模块的饮用路径，字符串
# 自定义存储模块必须实现save和close接口
STORAGE_MODUL = 'base.dbs.Local'

# 存储配置
STORAGE_CONFIG = {
    'file_path': os.path.join(os.getcwd(), 'files'),
    'mode': 'a+',
    'encoding': 'utf-8',
    'size': '100M',
    'filename': 'spider_file.txt'
}
# STORAGE_CONFIG = {
#     'type': 'mysql',
    # 'host': 'localhost',
    # 'port': int,
    # 'username': '',
    # 'password': '',
    # 'db': '',
    # 'tablename': '',
# }

QUEUE_MODUL = 'base.queues.Rabbitmq'

# 队列地址
QUEUE_CONFIG = {
    # 'host': 'localhost',
    # 'port': 10000,
    # 'authkey':b'spider',
    'host': '192.168.3.30',
    'port': 5672,
    'username': 'admin',
    'password': '880326',
}

# 下载延时，针对线程
DELAY = 0

# 一个爬虫注册容器，所有爬虫需要再次注册
SPIDERS = []
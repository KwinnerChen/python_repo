import os

# 下载线程数
DOWNLOAD_THREAD_NUM = 1

# 解析线程数
PARSER_THREAD_NUM = 1

# 存储线程
STORAGE_THREAD_NUM = 1

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

QUEUE_MODUL = 'base.queues.rabbitmq'

# 队列地址
QUEUE_CONFIG = {
    # 'host': 'localhost',
    # 'port': 10000,
    # 'authkey':b'spider',
    'host': '192.168.3.30',
    'port': 5672,
    'username': 'admin',
    'password': 'admin',
}

# 下载延时，针对线程
DELAY = 0

# 一个爬虫注册容器，所有爬虫需要再次注册
SPIDERS = []
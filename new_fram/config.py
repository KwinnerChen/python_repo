## 下载线程数
# DOWNLOAD_THREAD_NUM = 1


## 解析线程数
# PARSER_THREAD_NUM = 1


## 存储线程数
# STORAGE_THREAD_NUM = 1


## 下载任务重试次数，0表示不重试，重试任务会被重新放入当前队列末尾
# RETRY_TIMES = 0

# 存储模块引用
STORAGE_MODUL = 'base.dbs.Mysql'

# 存储配置
STORAGE_CONFIG = {
    'host': '192.168.3.30',
    'port': 3306,
    'user': 'root',
    'password': 'Ck@880326',
    'db': 'test_learn',
}


## 队列地址配置，默认使用本地队列
# QUEUE_ADDRESS = {
#     'host': 'localhost',
#     'port': 10000,
#     'authkey':b'spider',
# }


## 请求延时，是每个下载线程的主动堵塞时间
# DELAY = 0


## 每个定义的爬虫类必须在此注册，否则无法运行
# SPIDERS = []

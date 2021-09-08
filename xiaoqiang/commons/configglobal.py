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
STORAGE_MODUL = None

# 存储配置
STORAGE_CONFIG = {
    'host': 'localhost',
    'port': int,
    'username': '',
    'password': '',
    'db': '',
}

# rabbitmq队列配置
QUEUE_CONFIG = {
    'host': '192.168.3.30',
    'port': 5672,
    'username': 'admin',
    'password': '880326',
    'vhost': '/',
}

# 下载延时，针对线程
DELAY = 0

# 一个爬虫注册容器，所有爬虫需要再次注册
SPIDERS = []

# 默认值为True，将显示更多细节
DEBUG = True

# 日志文件路径
LOG_FILE_PATH = os.path.join(os.getcwd(), 'logs')

# 请求中间件
MIDDLEWARE = []

# 事件通知
NOTIFIER = None

# 事件通知服务配置
NOTIFIER_CONFIG = {

}

# 使用的执行器
EXECUTOR = None

# 下载器
DOWNLOADER = None
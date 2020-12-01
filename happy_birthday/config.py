import os
from dbmodule.utils import DBType


# 运行端口
PORT = 8000

# 静态文件路径
STA_PATH = os.path.join(os.getcwd(), "static")

# 图片文件夹路径
IMG_PATH = os.path.join(os.getcwd(), "images")

# html模版文件地址
TEM_PATH = os.path.join(os.getcwd(), "static", "templates")

# css文件地址
CSS_PATH = os.path.join(os.getcwd(), "static", "css")

# js文件地址
JS_PATH = os.path.join(os.getcwd(), "static", "js")

# 用于Applacatino类实例的关键字参数
settings = {
    "static_path": STA_PATH,
    "cookie_secret": "happy birthday",
    "xsrf_cookies": True,
    "debug" : True,
}

# 数据库配置
DB = {
    "db_type": DBType.Mysql,
    "db_name": "HappyBirthday",
    "host": "192.168.3.30",
    "port": 3306,
    "user": "root",
    "password": "Ck@880326"
}

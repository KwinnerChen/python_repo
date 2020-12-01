#!/user/bin/env python3
# -*- coding: utf-8 -*-


import sys
import config
from tornado.web import Application
from tornado.ioloop import IOLoop
from handlers import *


def run(port):
    app = Application((
        (r'/', MainHandler),
        (r'/login', MainHandler),
        (r'/js/(?P<filename>.*?\.js)', JsHandler),
        (r'/css/(?P<filename>.*?\.css)', CssHandler),
        (r'/images/(?P<filename>.*?\.jpg|png)', ImagesHandler),
        (r'/birthday', BirthdayHandler),
    ),
    **config.settings)
    app.listen(port)
    IOLoop.current().start()


def shutdown():
    IOLoop.current().stop()
    

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            run(int(config.PORT))
        else:
            port = sys.argv[1]
            assert len(sys.argv) <= 2, "运行只需要一个端口号，多余参数将被忽略！"
            assert port.isdigit(), "端口应是数字，且不要占用保留端口！"
            run(int(port))
    except KeyboardInterrupt:
        print("停机。。。")
    except Exception as e:
        print(e)
    finally:
        shutdown()
        print("shutdown server.....")
    
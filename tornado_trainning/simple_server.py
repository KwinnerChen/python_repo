#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import tornado.web
import tornado.ioloop
import asyncio
from datetime import datetime


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write("hello tornado")
        self.finish()
        print("%s %s %s %s %s %s %s" % (datetime.now().strftime("%Y.%m.%d-%H:%M:%S"), self.request.method, self.request.uri, self.request.version, self.request.host, 200, "OK"))


settings = {
    'Debug': True,
}

def main():
    try:
        app = tornado.web.Application(
            (
                ('/', MainHandler),
            ),
            **settings
        )
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass
    finally:
        print("server shutting down....")


if __name__ == '__main__':
    main()
    
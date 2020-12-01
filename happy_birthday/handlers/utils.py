# -*- coding: utf-8 -*-


from tornado.web import RequestHandler
from config import TEM_PATH
from tornado.log import logging


class BaseHandler(RequestHandler):
    def get_template_path(self):
        return TEM_PATH

    def on_finish(self):
        pass

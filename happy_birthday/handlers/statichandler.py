# -*- coding: utf-8 -*-


__all__ = ["ImagesHandler", "JsHandler", "CssHandler"]


from .utils import BaseHandler
from config import IMG_PATH, JS_PATH, CSS_PATH
from os.path import join as join_path


class ImagesHandler(BaseHandler):
    async def get(self, filename):
        img = self.__get_file(filename)
        self.write(img)
        
    def __get_file(self, filename):
        path = join_path(IMG_PATH, filename)
        with open(path, 'rb') as f:
            return f.read()


class JsHandler(BaseHandler):
    async def get(self, filename):
        file = self.__get_file(filename)
        self.write(file)

    def __get_file(self, filename):
        path = join_path(JS_PATH, filename)
        with open(path, 'rb') as f:
            return f.read()


class CssHandler(BaseHandler):
    async def get(self, filename):
        file = self.__get_file(filename)
        self.write(file)

    def __get_file(self, filename):
        path = join_path(CSS_PATH, filename)
        with open(path, 'rb') as f:
            return f.read()
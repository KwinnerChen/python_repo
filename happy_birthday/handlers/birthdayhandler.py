# -*- coding: utf-8 -*-


from .utils import BaseHandler
from config import IMG_PATH
import os.path


class BirthdayHandler(BaseHandler):
    async def get(self):
        await self.render("photowall.html")

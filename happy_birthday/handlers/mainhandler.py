# -*- coding: utf-8 -*-


from .utils import BaseHandler


class MainHandler(BaseHandler):
    async def get(self):
        await self.render("index.html")
        
    async def post(self):
        name = self.get_body_argument("name")
        date = self.get_body_argument("birthday")
        print(name, date)
        self.redirect("/birthday")

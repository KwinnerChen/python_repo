#! usr/bin/env python3
# -*- coding: utf-8 -*-


import re
from lxml import etree


class Selector:
    def __init__(self, response, coding=None):
        self.response = response
        self.coding = coding
        self.text = self.__get_text()
        self.content = response.content
        self.tree = etree.HTML(self.text)

    def __get_text(self):
        if self.coding:
            return self.response.content.decode(self.coding)
        else:
            return self.response.text

    def xpath(self, xpex, string=None):
        if not string:
            return self.tree.xpath(xpex)
        else:
            tree = etree.HTML(string)
            return tree.xpath(xpex)

    def findall(self, regexp, string=None):
        if not string:
            return re.findall(regexp, self.text)
        else:
            return re.findall(regexp, string)

    def search(self, regexp, string=None):
        if not string:
            return re.search(regexp, self.text)
        else:
            return re.search(regexp, string)

    

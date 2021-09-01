# -*- coding: utf-8 -*-


"""
这是一个用于通知的模块，例如邮件等。
"""


import abc
import os
import smtplib
import json


class Notifier(abc.ABC):
    @abc.abstractmethod
    def notify(self, message: str):
        """
        发送邮件到指定收件人列表
        """


class Email(Notifier):

    def __init__(self, addr, port, user, password) -> None:
        self. addr = addr
        self.user = user
        self.passworld = password
        self.port = port

    @staticmethod
    def __get_receivers():
        """
        获取收件人列表
        """
        with open(os.path.join(os.getcwd(), "contacts.json"), "r") as f:
            return json.loads(f)

    def notify(self, message: str):
        contacts = self.__get_receivers()

        with smtplib.SMTP(self.addr, self.port) as smtp:
            smtp.login(self.user, self.passworld)
            return smtp.sendmail(
                self.user,
                contacts,
                message
            )
            

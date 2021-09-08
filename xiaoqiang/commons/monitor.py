# -*- coding: utf-8 -*-


"""
这是一个用于通知的模块，例如邮件等。
"""


import abc
import os
import smtplib
import json


class Notifier(abc.ABC):
    def __init__(self, config) -> None:
        self.config = config

    @abc.abstractmethod
    def notify(self, message: str):
        """
        发送邮件到指定收件人列表
        """


class Email(Notifier):

    def __init__(self, config) -> None:
        super().__init__(config)
        self.user = config.NOTIFIER_CONFIG['user']
        self.password = config.NOTIFIER_CONFIG['password']
        self.addr = config.NOTIFIER_CONFIG['addr']
        self.port = config.NOTIFIER_CONFIG['port']

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
            smtp.login(self.user, self.password)
            return smtp.sendmail(
                self.user,
                contacts,
                message
            )
            

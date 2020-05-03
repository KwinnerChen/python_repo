#! /usr/bin/env python3
# -*- coding: utf-8 -*-


'''
单线程顺序下载20张图片保存在本地
'''


import os
import time
import sys
import requests


POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL = 'http://flupy.org/data/flags'
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)


def save_flag(img, filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'wb') as f:
        f.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):
    for cc in cc_list:
        img = get_flag(cc)
        show(cc)
        save_flag(img, cc.lower()+'.gif')
    return len(cc_list)


def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
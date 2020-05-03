#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from collections import deque


def get_coroutines():
    rep = None
    while True:
        print('will yield', rep)
        url = yield rep
        print(url)
        if url is None:
            break
        rep = requests.get(url)
        

def main():
    gen = get_coroutines()
    yield from gen


if __name__ == '__main__':
    result = []
    gen = main()
    next(gen)
    for url in ('http://www.baidu.com', 'http://www.sina.com', 'http://www.163.com'):
        r = gen.send(url)
        result.append(r)
    # gen.send(None)
    gen.close()
    print(result)
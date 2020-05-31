#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from collections import deque
import asyncio
from queue import Queue
import time


# def get_coroutines():
#     rep = None
#     while True:
#         print('will yield', rep)
#         url = yield rep
#         print(url)
#         if url is None:
#             break
#         rep = requests.get(url)
        

# def main():
#     gen = get_coroutines()
#     yield from gen


async def downloader(url):
    resp = requests.get(url)
    return resp


def downloader_ord(url):
    return requests.get(url)


async def worker(q_task):
    while True:
        if q_task.empty():
            continue
        url = q_task.get()
        print('get %s' % url)
        if url is None:
            break
        resp = await downloader(url)
        print(resp.text[:100])
        print()


async def main(coro_num):
    q_task = Queue()
    for url in ('http://www.baidu.com',) * 20:
        q_task.put(url)
    for i in range(coro_num):
        q_task.put(None)
    for i in range(coro_num):
        task1 = asyncio.create_task(worker(q_task))
        await task1


def main_ord():
    q_task = Queue()
    for url in ('http://www.baidu.com',) * 50:
        q_task.put(url)
    q_task.put(None)
    while True:
        if q_task.empty():
            continue
        url = q_task.get()
        print("get: %s" % url)
        if url is None:
            break
        resp = downloader_ord(url)
        print(resp.text[:100])




if __name__ == '__main__':
    # result = []
    # gen = main()
    # next(gen)
    # for url in ('http://www.baidu.com', 'http://www.sina.com', 'http://www.163.com'):
    #     r = gen.send(url)
    #     result.append(r)
    # # gen.send(None)
    # gen.close()
    # print(result)
    ts = time.time()
    asyncio.run(main(1))
    # main_ord()
    te = time.time()
    print('耗时：%.2e s' % (te-ts))
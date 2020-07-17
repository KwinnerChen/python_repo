#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
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
    loop = asyncio.get_running_loop()
    r = await loop.run_in_executor(None, requests.get, url)
    return r


def downloader_ord(url):
    return requests.get(url)


async def worker(q_task):
    while True:
        if q_task.empty():
            continue
        url = await q_task.get()
        print('get %s' % url)
        if url is None:
            break
        resp = await downloader(url)
        print(resp.text[:100])
        print()
        q_task.task_done()


async def main(coro_num):
    coros = []

    q_task = asyncio.Queue()

    for url in ('http://www.baidu.com',) * 50:
        await q_task.put(url)
    
    for _ in range(coro_num):
        await q_task.put(None)

    for _ in range(coro_num):
        task1 = asyncio.create_task(worker(q_task))
        coros.append(task1)

    await asyncio.gather(*coros)


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
    asyncio.run(main(6))
    # main_ord()
    te = time.time()
    print('耗时：%.2e s' % (te-ts))
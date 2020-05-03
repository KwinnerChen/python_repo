#! /usr/bin/env python3
# -*- coding: utf-8 -*-


'''
协程并发下载flags
'''


import asyncio
import requests
import aiohttp
import os
import time
from flags import BASE_URL, save_flag, show, main, POP20_CC


async def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    print('%s start' % cc)
    async with aiohttp.request('GET', url) as reps:  # 此处必须使用上下文管理器
        img = await reps.read()
        return img


# async def get_flag(cc):  # 非完全异步
#     url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
#     print('%s start' % cc)
#     resp = requests.get(url)
#     return resp.content


async def download_one(cc):
    img = await get_flag(cc)
    show(cc)
    save_flag(img, cc+'.gif')
    return cc


async def download_many(cc_list):
    tasks = []
    for cc in cc_list:
        task = asyncio.create_task(download_one(cc))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def run(cc_list):
    t0 = time.time()
    res = await download_many(cc_list)
    print('{} flags downloaded in {:.2f}'.format(len(res), time.time()-t0))


if __name__ == '__main__':
    asyncio.run(run(POP20_CC[:5]))

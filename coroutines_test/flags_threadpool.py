#! /usr/bin/env python3
# -*- coding: utf-8 -*-


'''
使用线程池异步下载20张图片保存到本地
'''


from concurrent import futures
from flags import save_flag, get_flag, show, main


MAX_WORKERS = 20


def download_one(cc):
    img = get_flag(cc)
    show(cc)
    save_flag(img, cc+'.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, cc_list)
    return len(list(res))


if __name__ == '__main__':
    main(download_many)
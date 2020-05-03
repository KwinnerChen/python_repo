#! /usr/bin/evn python3 
# -*- coding: utf-8 -*-


'''
使用ThreadPoolExecutor的submit方法来返回future对象
'''


from concurrent import futures
from flags_threadpool import download_one, main


def download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in cc_list:
            future = executor.submit(download_one, cc)
            to_do.append(futures)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))

        results = []
        fiter = futures.as_completed(to_do)  # 运行时报错，why？？？？
        for f in fiter:
            res = f.result()
            msg = '{} result: {}'
            print(msg.format(f, res))
            results.append(res)
        return len(results)


if __name__ == '__main__':
    main(download_many)    

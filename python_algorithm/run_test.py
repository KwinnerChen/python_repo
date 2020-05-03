#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import random
import time


def main(fn, seq_len=20, rand=(0, 999, 2)):
    """
    构建一个随机列表用于测试排序算法，屏幕打印原始列表和排序后列表，
    并给出当前排序耗时。

    main(fn, seq_len:int, rand:(start, stop, step)) => dtime(s)

    params:
    :seq_len: 列表长度;
    :rand: 一个三元组，随机参数（start, stop, step)
    """

    query = [random.randrange(*rand) for i in range(seq_len)]
    print(f"原始列表是：{query}")
    print("\n")
    time1 = time.time()
    query = fn(query)
    time2 = time.time()
    print(f"升序排序后：{query}")
    return time2 - time1
    
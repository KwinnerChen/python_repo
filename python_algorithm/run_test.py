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

    seq = [random.randrange(*rand) for i in range(seq_len)]
    print(f"原始列表是：{seq}")
    print("\n")
    if fn.__code__.co_argcount == 1:
        time1 = time.time()
        seq = fn(seq)
        time2 = time.time()
    elif fn.__code__.co_argcount == 2:
        time1 = time.time()
        seq = fn(seq, len(seq)-1)
        time2 = time.time()
    print(f"升序排序后：{seq}")
    return time2 - time1
    
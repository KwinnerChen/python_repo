#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
不是协程练习，选择排序算法的实现
"""


from run_test import main


def ch_que(query):
    for i in range(len(query)-1):
        for j in range(i+1, len(query)):
            if query[i] > query[j]:
                query[i], query[j] = query[j], query[i]
    return query


if __name__ == '__main__':
    dtime = main(ch_que, seq_len=10000)
    print(f"耗时: {dtime}s")
    
#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
选择排序算法的实现
将每个元素和其后元素进行比较，是否更换位置
"""


from run_test import main


# 迭代实现
def ch_que(query):
    for i in range(len(query)-1):
        for j in range(i+1, len(query)):
            if query[i] > query[j]:
                query[i], query[j] = query[j], query[i]
    return query


# 递归实现
def ch_que_rec(seq, i):
    if i == 0:
        return
    j_max = i
    for j in range(i):
        if seq[j] > seq[j_max]:
            j_max = j
    seq[i], seq[j_max] = seq[j_max], seq[i]
    ch_que_rec(seq, i-1)
    return seq


if __name__ == '__main__':
    dtime = main(ch_que_rec)
    print(f"耗时: {dtime}s")
    
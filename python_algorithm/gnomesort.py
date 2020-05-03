#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
侏儒排序算法的python实现
"""


from run_test import main


def gnomesort(seq):
    i = 0
    while i < len(seq):
        if i == 0 or seq[i-1] <= seq[i]:
            i += 1
        else:
            seq[i-1], seq[i] = seq[i], seq[i-1]
            i -= 1
    return seq


if __name__ == '__main__':
    dtime = main(gnomesort, seq_len=10000)
    print(f"耗时：{dtime}")
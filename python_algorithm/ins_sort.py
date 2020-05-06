#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
插入排序的迭代和递归实现
最后元素和之前元素对比，是否交换位置
倒序比较万所有元素
"""


from run_test import main


# 递归版本
def ins_sort_rec(seq, i):
    if i == 0:
        return
    ins_sort_rec(seq, i-1)
    j = i
    while j > 0 and seq[j-1] > seq[j]:
        seq[j-1], seq[j] = seq[j], seq[j-1]
        j -= 1
    return seq


# 迭代版本
def ins_sort(seq, i):
    for i in range(1, len(seq)):
        j = i
        while j > 0 and seq(j-1) > seq(j):
            seq[j-1], seq[j] = seq[j], seq[j-1]
            j -= 1
    return seq


if __name__ == '__main__':
    main(ins_sort_rec)
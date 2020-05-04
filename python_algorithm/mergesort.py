#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from run_test import main


def mergesort(seq):
    mid = len(seq)//2
    left, right = seq[:mid], seq[mid:]
    # print(f"left: {left}")
    # print(f"right: {right}")
    if len(left) > 1:
        left = mergesort(left)
        # print(f"after letf: {left}")
    if len(right) > 1:
        right = mergesort(right)
    
    res = []
    while left and right:
        if left[-1] >= right[-1]:
            res.append(left.pop())
        else:
            res.append(right.pop())

    res.reverse()
    return (left or right) + res


if __name__ == '__main__':
    dtime = main(mergesort, seq_len=10)
    print(f"耗时：{dtime}")
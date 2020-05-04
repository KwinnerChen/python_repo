#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
实现一个L形砖块，拼凑成一个缺角棋盘
3  3  4  4  8  8  9  9
3  2  2  4  8  7  7  9
5  2  6  6 10 10  7 11
5  5  6  1  1 10 11 11
13 13 14  1 18 18 19 19
13 12 14 14 18 17 17 19
15 12 12 16 20 17 21 21
15 15 16 16 20 20 21 -1
"""


def cover(board, lab=1, top=0, left=0, side=None):
    if side is None:
        side = len(board)

    s = side // 2
    offsets = (0, -1), (side-1, 0)

    for dy_outer, dy_inner in offsets:
        for dx_outer, dx_inner in offsets:
            if not board[top+dy_outer][left+dx_outer]:
                board[top+s+dy_inner][left+s+dx_inner] = lab

    lab += 1
    if s > 1:
        for dy in [0, s]:
            for dx in [0, s]:
                lab = cover(board, lab, top+dy, left+dx, s)

    return lab


if __name__ == '__main__':
    board = [[0]*8 for i in range(8)]
    board[0][7] = -1
    cover(board)
    for row in board:
        print(" %2i" * 8 % tuple(row))
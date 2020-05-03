#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import threading
import itertools
import time
import sys


class Signal:  # 作者说python没有提共退出线程的API，所以需要设置一个退出标志。
    go = True  # 自我认为，python线程在返回函数之后会自动退出。只有在while循环的函数中需要给出退出标志。
               # 在某些时候Event对象比发送一个标志更适合。


def spin(msg, signal):  # 这里应该更适合使用Event对象
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = ' '.join((char, msg))
        write(status)
        flush()
        write('\r' * len(status))
        time.sleep(.1)
        if not signal.go:
            break
    write(' '*len(status) + '\r'*len(status))


def slow_function():
    time.sleep(3)
    return 42


def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=('thinking', signal))
    print('spinner object: ', spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result


def main():
    result = supervisor()
    print('Answer: ', result)


if __name__ == '__main__':
    main()
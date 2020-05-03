#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import itertools
import sys


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = ' '.join((char, msg))
        write(status)
        flush()
        write('\r' * len(status))
        await asyncio.sleep(.1)


async def slow_function():
    await asyncio.sleep(3)
    return 42


async def supervisor():
    task1 = asyncio.create_task(spin('thinking'))
    task2 = asyncio.create_task(slow_function())
    done, _ = await asyncio.wait((task1,task2), return_when=asyncio.FIRST_COMPLETED)
    print('\n')
    print(done.pop().result())


def main():
    asyncio.run(supervisor())


if __name__ == '__main__':
    main()
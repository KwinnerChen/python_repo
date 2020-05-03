#! usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, "hello"))  # 将需要等待的操作包装为可等待对象
    task2 = asyncio.create_task(say_after(2, "world"))  # 可等待对象包含协程，任务和Future对象
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


if __name__ == '__main__':
    asyncio.run(main())
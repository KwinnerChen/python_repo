#!usr/bin/env python3
# -*- coding: utf-8 -*-


"""
module for testing echo server
"""


import asyncio
from asyncio import tasks


async def echo_client(message: str):
    reader, writer = await asyncio.open_connection("192.168.3.7", 8080)

    print(f"send message: {message}")
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    message = data.decode()
    print(f"recieved message: {message}")

    print("close the connection")
    writer.close()


async def test():
    tasks = []
    for i in range(1000):
        task = echo_client(f"hello num {i}")
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(test())

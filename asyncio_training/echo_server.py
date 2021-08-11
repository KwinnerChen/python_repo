#!usr/bin/env python3
# -*- coding: utf-8 -*-


"""
a simple echo server
"""


import asyncio
import random
import sys


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = await reader.read(100)
    message = data.decode()

    addr = writer.get_extra_info("peername")
    print(f"recieved {message!r} from {addr!r}")

    await asyncio.sleep(random.randint(2, 10))
    print(f"send: {message!r}")
    writer.write(message.encode())
    await writer.drain()

    print("close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle,
        'localhost',
        8080
    )

    addr = server.sockets[0].getsockname()
    print(f"servering on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("shutdown server", file=sys.stderr)
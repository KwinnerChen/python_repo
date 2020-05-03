#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import asyncio
from charfinder import UnicodeNameIndex


CRLF = b'\r\n'
PROMPT = b'?>'
index = UnicodeNameIndex()


async def handle_queries(reader, writer):  # asyncio.StreamReader, asyncio.StreamWriter
    while True:
        writer.write(PROMPT)  # 非协程，将字节字符串写入流
        await writer.drain()  # 协程，刷新缓冲输出到客户端
        data = await reader.readline()  # 协程，从流中读取输入，字节字符串，可能需要等待从客户端返回
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = '\x00'
        client = writer.get_extra_info('peername')  # 返回与套接字连接的远程地址
        print("Received from {}: {!r}".format(client, query))
        if query:
            if ord(query[:1]) < 32:
                break
            lines = list(index.find_description_strs(query))
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)
            writer.write(index.status(query, len(lines)).encode() + CRLF)
            await writer.drain()  # 刷新缓冲，流输出
            print("Sent {} results".format(len(lines)))
    print("close the client socket")
    writer.close()


def main(address='127.0.0.1', port=2323):
    port = int(port)
    loop = asyncio.get_event_loop()  # 获取一个事件循环
    server_coro = asyncio.start_server(handle_queries, address, port,
                                       loop=loop)  # 创建一个指定事件循环的服务协程，是一个asyncio.Server实例
    server = loop.run_until_complete(server_coro)  # 接受一个Future对象或者协程对象，协程对象将会包装为Task对象，返回Future结果。
    host = server.sockets[0].getsockname()
    print("Serving on {}. Hit CTRL-C to stop.".format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("Server shutting down.")
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main(*sys.argv[1:])
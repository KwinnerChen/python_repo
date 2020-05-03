#! /usr/bin/env python3


import aiohttp
import asyncio
import sys
from charfinder import UnicodeNameIndex
from aiohttp import web

index = UnicodeNameIndex()


async def home(request):
    return web.Response(text=' '.join(chr(i) for i in range(10000)))
    # return web.Response(text='hello')


async def hello(request):
    return web.Response(text='hello!')


def main(address='127.0.0.1', port=8888):
    port = int(port)
    app_home = web.Application()
    app_home.router.add_get('/', home)
    app_home.router.add_get('/hello', hello)
    web.run_app(app_home, host=address, port=port)


if __name__ == '__main__':
    main()
from asyncio import sleep

from utils.helpers import *
import asyncio

def log(msg: str):
    print(f'{clock()} {msg}')


async def goo():
    log('goo works')
    await sleep(0.1)
    log('goo done')


async def foo():
    log('foo works')
    await sleep(2)
    log('foo done')


async def main_task():
    # await foo()
    # await goo()
    ftask = asyncio.create_task(foo())
    gtask = asyncio.create_task(goo())

    await sleep(5)
    log('main done')


if __name__ == '__main__':
    asyncio.run(main_task())  # tworzy event loop

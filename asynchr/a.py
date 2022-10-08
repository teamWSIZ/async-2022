from asyncio import sleep

from utils.helpers import *
import asyncio

def log(msg: str):
    print(f'{clock()} {msg}')


async def goo():
    log(f'goo works, thread: {tn()}, task:{task_name()}')
    await sleep(0.1)
    log('goo done')


async def foo():
    log(f'foo works, thread: {tn()}, task:{task_name()}')
    await sleep(2)
    log('foo done')


async def main_task():
    log(f'main; thread: {tn()}, task:{task_name()}')
    # await foo()
    # await goo()
    ftask = asyncio.create_task(foo())
    gtask = asyncio.create_task(goo())
    log(f'main, zadania już zaschedulowane; thread: {tn()}, task:{task_name()}')


    await sleep(5)
    log('main done')


if __name__ == '__main__':
    print(f'thread: {tn()}')
    asyncio.run(main_task())  # tworzy event loop

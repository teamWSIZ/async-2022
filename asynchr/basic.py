import math
from asyncio import sleep

from utils.helpers import *
import asyncio


def log(msg: str):
    line = f'{clock()} {msg}'
    buf.log(line)


class BufLogger:
    def __init__(self):
        self.lines = ['' for _ in range(100)]
        self.N = 100
        self.i = 0

    def log(self, msg):
        self.lines[self.i % self.N] = msg
        self.i += 1

    def print(self):
        for i in range(self.i):
            print(self.lines[i])
        self.i = 0


buf = BufLogger()


async def the_quick_task():
    log(f'quick works,  task:{task_name()}')
    await sleep(0.1)  # np. sprawdzenie dostności IP; typu ping
    log('quick done')


async def the_important_task():
    log(f'important works,  task:{task_name()}')
    await sleep(0.5)  # np. ściągnięcie 100MB z sieci
    log('important done')


async def the_secret_task() -> int:
    log(f'secret works,  task:{task_name()}')
    await sleep(0.5)  # np. ściągnięcie 100MB z sieci
    log('secret done')
    return 11


async def scheduler():
    log(f'scheduler; task:{task_name()}')  # thread: MainThread
    # await foo()
    # await goo()
    ftask = asyncio.create_task(the_quick_task())
    gtask = asyncio.create_task(the_important_task())
    # log('ftask done? ' + str(ftask.done()))
    # await ftask
    # log('ftask done? ' + str(ftask.done()))

    await asyncio.gather(ftask, gtask)
    log('oba skończone')    # 40 usec??

    stask = asyncio.create_task(the_secret_task())
    await sleep(0)
    log(f'scheduler, zadania już zaschedulowane, task:{task_name()}')
    f = 0
    for i in range(10 ** 6):
        f += math.sin(i)
    log(f'suma sinusów {f:.3f}')

    secret = await stask
    log(f'{secret=}')

    await sleep(2)
    log('scheduler done')


if __name__ == '__main__':
    # print(f'thread: {tn()}') #thread: MainThread
    asyncio.run(scheduler())  # tworzy event loop
    buf.print()

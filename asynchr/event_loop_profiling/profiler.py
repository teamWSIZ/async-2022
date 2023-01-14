import asyncio
import time
from asyncio import run, create_task
from random import randint

from asynchr.utils import *  # tu dać import na file z funkcjami typu log(), task_name() itp
import matplotlib.pyplot as plt


def format_report(q_values):
    q_values = [q * 1000 for q in q_values]
    s = f'[{q_values[0]:.3f}'
    for v in q_values:
        s += ',' + f'{v:.3f}'
    s += ']'
    return s


def get_percentiles(delays: list[float], quantiles: list[float]):
    delays.sort()
    n = len(delays)
    q_values = [delays[int(n * q)] for q in quantiles]
    # for (q, v) in zip(quantiles, q_values):
    #     print(f'p[{q:.3f}]={v:.5f}')
    return q_values


async def watcher():
    log(f'watcher works, thread: {tn()}, task: {task_name()}')
    previous = ts()
    delays = []
    while True:
        await asyncio.sleep(0.001)
        delay = ts() - previous
        previous = ts()
        delays.append(delay - 0.001)
        if len(delays) > 600:
            break
    print(format_report(get_percentiles(delays, [0.01, 0.05, 0.50, 0.95, 0.99])))
    plt.hist(delays, bins=60)
    plt.show()


async def useful_work():
    while True:
        if randint(0, 5) == 0:
            # time.sleep(randint(0, 10) * 0.0000100)
            time.sleep(0.0001)
        await asyncio.sleep(0.0001)


async def main():
    log(f'works, thread: {tn()}, task: {task_name()}')
    create_task(useful_work())
    create_task(watcher())
    await asyncio.sleep(1)


if __name__ == '__main__':
    run(main())

from asyncio import run, Queue, create_task, gather, sleep, Task
from collections.abc import Coroutine

from asynchr.utils.helpers import log


async def worker(id_: int, q: Queue):
    log(f'worker {id_=} starting work...')
    while True:
        item_to_work_on = await q.get()
        if item_to_work_on == 666: break
        log(f'worker {id_=} works on {item_to_work_on}')
        await sleep(0.2)
    log(f'worker {id_=} done')


async def main():
    q = Queue(maxsize=3)
    w: list[Task] = []
    n_workers = 3

    for i in range(n_workers):
        w.append(create_task(worker(i, q)))
    log('boss takes an early morning coffee break ... ')
    await sleep(0.5)
    for i in range(10):
        log(f'boss tries to put item {i} onto queue')
        await q.put(i)
    log('boss done for the day...')
    # todo: poczekać aż kolejka będzie pusta... ??
    for i in range(n_workers): await q.put(666)
    await gather(*w)


if __name__ == '__main__':
    run(main())

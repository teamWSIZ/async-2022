from asyncio import run, sleep, create_task, gather

from scratch.helpers import log


async def short_task():
    log('start short')
    await sleep(0.2)
    log('end short')
    return 1


async def long_task():
    log('start long')
    await sleep(1.)
    log('end end')
    return 2


async def main():
    s = create_task(short_task())
    l = create_task(long_task())
    # ???
    r1, r2 = await gather(s, l)
    print(r1, r2, r1 + r2)


if __name__ == '__main__':
    run(main())

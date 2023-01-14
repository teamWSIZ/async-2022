from asyncio import sleep, create_task, run


async def blink(n: int):
    for i in range(n):
        print('blink')
        await sleep(0.2)


async def main():
    for i in range(10000):
        if i % 5 == 0:
            print(f'{i=}')
            create_task(blink(3))
        await sleep(1)


if __name__ == '__main__':
    run(main())
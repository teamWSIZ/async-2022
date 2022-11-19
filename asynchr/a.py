from asyncio import sleep, run

async def goo():
    print('ok')

def blah():
    print('workz')

async def foo():
    await sleep(0.2)
    await goo()
    blah()




if __name__ == '__main__':
    run(foo())

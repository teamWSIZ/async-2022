from asyncio import run, sleep, create_task, gather, Event
from dataclasses import dataclass

from asynchr.utils.helpers import log


@dataclass
class Pizza:
    status: str = 'only ingredients'


async def client(pizza: Pizza, token: Event):
    log(f'klient rozpoczyna czekanie... {pizza=}')
    # while pizza.status != 'ready':
    #     log(f'damn; pizza still {pizza=}')
    #     await sleep(0.1)

    await token.wait()

    log(f'wow! -- finally, {pizza=}')
    log(f'eating...')
    await sleep(5)
    log(f'eating done')


async def main():
    # kod pizzerii ...
    log('otwieramy pizzerie')
    pizza = Pizza()
    token1 = Event()
    client_in_house = create_task(client(pizza, token1))
    await sleep(1.0)
    pizza.status = 'in oven'
    await sleep(2.0)
    pizza.status = 'ready'
    token1.set()

    await client_in_house
    log('zamykamy pizzerie')


if __name__ == '__main__':
    run(main())

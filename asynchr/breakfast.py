


"""
Śniadanie;
- zagotować wodę (0.3 sek); boil_water -> water
- zaparzyć kawę (potrzebuje wodę; 0.2 s); make_caffe –> cafee
- pokroić chleb (0.1 s); cut_bread -> bread
- posmarować masłem chleb (0.1 s); prepare_bread; wymaga "bread" -> good_bread
- zagotować jajka (0.4 s); boil_eggs; -> eggs
- przygotować stół (0.1 s); wymaga: cafee, good_bread, eggs


Zadanie -- napisać funkcje jak ↑↑, np. async def make_cafee(water: int) -> int

A) Napisać odpowiednie funkcje jak ↑↑
B) Napisać funckę async def scheduler, który wykona przygotowanie śnidania zgodnie z przepisem

"""
import asyncio
from asyncio import sleep

from asynchr.utils.helpers import clock


def log(msg: str):
    line = f'{clock()} {msg}'
    print(line)




async def boil_water() -> str:
    log('boiling water ...')
    await sleep(0.3)
    log('waterd boiling done!')
    return 'water'

async def make_caffe() -> str:
    log('making caffe ...')
    water = await boil_water()
    log('have water...')
    await sleep(0.2)
    log('caffe done!')
    return 'caffe'


async def prepare_bread() -> str:
    #.... stub
    return 'good bread'




async def scheduler():
    c = asyncio.create_task(make_caffe())
    b = asyncio.create_task(prepare_bread())

    # gather

    #prepare table

    # i odczytać ile to trwało...





if __name__ == '__main__':
    asyncio.run(scheduler())
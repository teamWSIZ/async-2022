import asyncio
from asyncio import sleep, create_task, Event
from enum import Enum
from random import randint
from collections import deque
from uuid import uuid4

from asynchr.basic import log
from asynchr.utils.helpers import clock, tn, task_name


class S(Enum):
    WHEEL_ON = 0
    WHEEL_OFF = 1


def log(msg: str):
    line = f'{clock()} [{task_name()}] {msg}'
    print(line)


class Car:
    def __init__(self):
        self.car_id = randint(0, 1000)
        self.lifted = False
        self.fuel = 100  # 0..100   % of full
        self.wheels = [S.WHEEL_ON] * 4
        self.wheel_state = [30] * 4  # 0..100   % of the new one
        self.in_service = False
        self.token_string = ''

    def __str__(self):
        return f'(car id={self.car_id})'

    def __repr__(self):
        return str(self.__dict__)


class CarService:

    def __init__(self):
        self.car: Car = None  # auto obecnie serwisowane...
        self.car_queue = deque()
        self.car_ready_tokens: dict[str, Event] = dict()

    def get_ready_token(self, token_string: str) -> Event:
        return self.car_ready_tokens[token_string]

    async def assign_car_for_service(self, car: Car) -> str:
        """Client brings his car for service; we take it (immediately) and give him a string,
        which can be converted into token (Event) that can be awaited on"""
        log(f'client assigns car {car}')
        self.car_queue.append(car) #fixme
        # log(f'car {car} entering service')
        # self.car = car
        # create_task(self.service_car())  # raczej powinniśmy mieć taski dla zespołów... które
        token = self.__generate_token()
        self.car_ready_tokens[token] = Event()
        car.token_string = token


    def __generate_token(self) -> str:
        return str(uuid4())[:6]

    async def __schedule_for_service(self):
        while True:
            # sprawdź czy są elementy w self.car_queue
            # jeśli tak, to poczekaj aż self.car = None, i weź element z self.car_queue
            pass
        # while self.car is not None:
        #     await sleep(0.1)

    async def __release_car(self) -> Car:
        # fixme: do final checks?
        c = self.car
        log(f'releasing {self.car}')
        # oznaczamy token odpowiedzialny za poinformowanie klienta o gotowym samochodzie
        self.car_ready_tokens[self.car.token_string].set()
        self.car = None

        return c

    async def service_car(self) -> Car:
        """
        Services the self.car
        Do the needfull (up, down, change wheels if they are below 50%)
        """
        log(f'servicing {self.car}')
        await sleep(0.4)
        log(f'done with service of {self.car}')
        return await self.__release_car()

    async def __change_wheel(self, wheel_number):
        # check car is UP (if not -- wait until it is)
        # check wheel_state; if < 50 --- wheel must be changed (and get wheel_state=100)
        #   - firstly, take the wheel off (200ms  (later + random..))
        #   - replate the wheel (state -> 100) (300ms (later + random))
        #   - put wheel on (100ms + random) --> self.wheels[wheel_number] should now be S.WHEEL_ON
        pass


async def main():
    car1 = Car()
    car2 = Car()
    car3 = Car()
    car4 = Car()
    car_service = CarService()
    await car_service.assign_car_for_service(car1)
    await car_service.assign_car_for_service(car2)
    await car_service.assign_car_for_service(car3)
    await car_service.assign_car_for_service(car4)

    # car = await car_service.service_car()
    await sleep(3)  # fixme: otherwise tasks created per create_tasks will not finish...


if __name__ == '__main__':
    asyncio.run(main())

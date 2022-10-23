import asyncio
from asyncio import sleep, create_task
from enum import Enum
from random import randint
from collections import deque

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

    def __str__(self):
        return f'(car id={self.car_id})'

    def __repr__(self):
        return str(self.__dict__)


class CarService:

    def __init__(self):
        self.car = None
        self.car_queue = deque()


    async def schedule_for_service(self):
        while True:
            # sprawdź czy są elementy w self.car_queue
            # jeśli tak, to poczekaj aż self.car = None, i weź element z self.car_queue
            pass
        # while self.car is not None:
        #     await sleep(0.1)

    async def take_car(self, car: Car):
        """Take the car for service; must be sure that only 1 car is in service at any time"""
        log(f'taking up car {car}')
        self.car_queue.append(car)
        log(f'car {car} entering service')
        self.car = car
        create_task(self.service_car())

    async def release_car(self) -> Car:
        # fixme: do final checks?
        c = self.car
        log(f'releasing {self.car}')
        self.car = None
        return c

    async def service_car(self) -> Car:
        # do the needfull (up, down, change wheels if they are below 50%)
        log(f'servicing {self.car}')
        await sleep(0.4)
        log(f'done with service of {self.car}')
        return await self.release_car()

    async def change_wheel(self, wheel_number):
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
    await car_service.take_car(car1)
    await car_service.take_car(car2)
    await car_service.take_car(car3)
    await car_service.take_car(car4)

    # car = await car_service.service_car()
    await sleep(3)  # fixme: otherwise tasks created per create_tasks will not finish...


if __name__ == '__main__':
    asyncio.run(main())

import asyncio
from enum import Enum


class S(Enum):
    WHEEL_ON = 0
    WHEEL_OFF = 1


class Car:
    def __init__(self):
        self.lifted = False
        self.fuel = 100  # 0..100   % of full
        self.wheels = [S.WHEEL_ON] * 4
        self.wheel_state = [30] * 4  # 0..100   % of the new one

    def __str__(self):
        return str(self.__dict__)


class CarService:

    def __init__(self):
        self.car = None

    async def take_car(self, car: Car):
        """Take the car for service; must be sure that only 1 car is in service at any time"""
        self.car = car

    async def release_car(self) -> Car:
        # do final checks?
        return self.car

    async def service_car(self) -> Car:
        # do the needfull (up, down, change wheels if they are below 50%)
        return await self.release_car()

    async def change_wheel(self, wheel_number):
        # check car is UP (if not -- wait until it is)
        # check wheel is WHEEL_OFF or WHEEL_OLD
        # if WHEEL_OLD -- take it off first (200ms)
        # if WHEEL_OFF -- put new wheel on, and set WHEEL_ON (300ms)
        pass


async def main_function():
    car = Car()
    car_service = CarService()
    await car_service.take_car(car)
    car = await car_service.service_car()


if __name__ == '__main__':
    asyncio.run(main_function())

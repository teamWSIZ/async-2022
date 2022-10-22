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
        self.in_service = False

    def __str__(self):
        return str(self.__dict__)


class CarService:

    def __init__(self):
        self.car = None

    async def take_car(self, car: Car):
        """Take the car for service; must be sure that only 1 car is in service at any time"""
        # have to wait until self.car = None
        self.car = car

    async def release_car(self) -> Car:
        # do final checks?
        return self.car

    async def service_car(self) -> Car:
        # do the needfull (up, down, change wheels if they are below 50%)
        return await self.release_car()

    async def change_wheel(self, wheel_number):
        # check car is UP (if not -- wait until it is)
        # check wheel_state; if < 50 --- wheel must be changed (and get wheel_state=100)
        #   - firstly, take the wheel off (200ms  (later + random..))
        #   - replate the wheel (state -> 100) (300ms (later + random))
        #   - put wheel on (100ms + random) --> self.wheels[wheel_number] should now be S.WHEEL_ON
        pass


async def main_function():
    car = Car()
    car_service = CarService()
    await car_service.take_car(car)
    car = await car_service.service_car()


if __name__ == '__main__':
    asyncio.run(main_function())

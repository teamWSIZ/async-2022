from asynchr.utils.helpers import log


class Service:
    def __init__(self):
        pass

    async def initialize(self):
        log('async part of initialization of Service')

    async def my_exciting_async_job(self, id: int):
        log(f'running job {id}')

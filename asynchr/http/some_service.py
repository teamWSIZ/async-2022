from asynchr.utils.helpers import log


class Service:
    def __init__(self):
        pass

    async def initialize(self):
        log('async part of initialization of Service')
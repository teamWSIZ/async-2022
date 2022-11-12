from asyncio import Event, run, sleep, create_task, gather


class Event2FA:

    def __init__(self):
        self.__event1 = Event()
        self.__event2 = Event()

    def is_set(self) -> bool:
        # both must be set() in order to return True
        return self.__event1.is_set() and self.__event2.is_set()

    def set(self, event_id: int):
        # set the __event with the number indicated by `event_id`
        if event_id == 1:
            self.__event1.set()
        elif event_id == 2:
            self.__event2.set()

    def clear(self):
        # clear both __event's
        self.__event1.clear()
        self.__event2.clear()

    async def wait(self):
        # both __event's must be set in order to proceed
        await self.__event1.wait()
        await self.__event2.wait()

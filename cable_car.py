from asyncio import Queue, sleep, create_task
from dataclasses import dataclass
from uuid import uuid4

from asynchr.basic import log


@dataclass
class Gondola:
    passengers: int
    places: int = 8
    gid = str(uuid4())[:4]


async def cable_car_loop(station: 'CCStation', gondola_time_delay: float):
    # fixme: add way to stop and exit this loop
    while True:
        log('New gondola is coming to station')
        await station.new_gondola_arrives(Gondola(passengers=0))
        await sleep(gondola_time_delay)


class CCStation:

    def __init__(self, initial_time_delay: float):
        self.gondola = Gondola(0)  # first gondola already awaits passengers
        self.passenger_queue = Queue()
        self.gondola_time_delay = initial_time_delay

    def start_cable_car(self):
        # start async function (infinite loop) that brings a new "gondola" (self.new_gondola_arrives()) every 2 seconds
        create_task(cable_car_loop(self, self.gondola_time_delay))

    async def new_gondola_arrives(self, new_gondola: Gondola):
        # once a new gondola one arrives, the previous one must leave (self.launch_gondola())
        await self.launch_gondola()
        self.gondola = new_gondola

    async def launch_gondola(self):
        # print a log line with self.gondola, await some 0.1s, set self.gondola = None
        log(f'Gondola leaves station: {self.gondola}')

    async def enqueue_passenger(self):
        # if gondola is waiting and not full -- embark it!; else wait
        await self.passenger_queue.put(True)

from asyncio import sleep, Event, create_task
from unittest import IsolatedAsyncioTestCase

from asynchr.utils.helpers import ts


def log(msg):
    print(msg)


async def set_event_after_time(e: Event, time: float):
    await sleep(time)
    e.set()

class Test(IsolatedAsyncioTestCase):

    def setUp(self):
        log('setup')

    async def asyncSetUp(self):
        log('async setup')

    async def asyncTearDown(self):
        log('async terdown')

    async def test_response1(self):
        log('test1')
        await sleep(0.2)
        log('test1 done')

    async def test_event(self):
        e = Event()
        st = ts()
        create_task(set_event_after_time(e, 0.5))
        await e.wait()
        en = ts()
        assert abs(en-st - 0.5) < 0.01

    async def test_event_is_set(self):
        e = Event()
        create_task(set_event_after_time(e, 0.5))
        await sleep(0.495)
        assert not e.is_set()
        await sleep(0.01)
        assert e.is_set()

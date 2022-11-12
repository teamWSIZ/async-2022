from asyncio import sleep, create_task
from unittest import IsolatedAsyncioTestCase

from asynchr.utils.helpers import ts
from two_fa_event import Event2FA


def log(msg):
    print(msg)


async def set_event_after_time(e: Event2FA, event_id: int, time: float):
    await sleep(time)
    e.set(event_id)


EVEN_DELAY1 = 0.2
EPS = 0.01
PRECISION = 2


class Test(IsolatedAsyncioTestCase):

    async def test_simple(self):
        e = Event2FA()
        st = ts()

        e.set(1)
        e.set(2)

        await e.wait()

        en = ts()
        assert abs(en - st - 0.00) < EPS

    async def test_set_second_event_after_some_time1(self):
        e = Event2FA()
        st = ts()

        e.set(1)
        create_task(set_event_after_time(e, 2, EVEN_DELAY1))

        await e.wait()

        en = ts()
        assert abs(en - st - EVEN_DELAY1) < EPS

    async def test_set_second_event_after_some_time2(self):
        e = Event2FA()
        st = ts()

        e.set(2)
        create_task(set_event_after_time(e, 1, EVEN_DELAY1))

        await e.wait()

        en = ts()
        assert abs(en - st - EVEN_DELAY1) < EPS

    async def test_set_both_events_after_02_sec(self):
        e = Event2FA()
        st = ts()

        create_task(set_event_after_time(e, 1, EVEN_DELAY1))
        create_task(set_event_after_time(e, 2, EVEN_DELAY1))

        await e.wait()

        en = ts()
        duration = en - st
        self.assertAlmostEqual(duration, EVEN_DELAY1, places=PRECISION,
                               msg='Both events set with same delay must define delay of Event2FA')

    async def test_cleared_events_block(self):
        # arrange
        e = Event2FA()
        st = ts()
        e.set(1)
        e.set(2)

        # act
        e.clear()
        create_task(set_event_after_time(e, 1, EVEN_DELAY1))
        create_task(set_event_after_time(e, 2, EVEN_DELAY1))
        await e.wait()  # must block for EVEN_DELAY1

        # assert
        en = ts()
        duration = en - st
        self.assertAlmostEqual(duration, EVEN_DELAY1, places=PRECISION,
                               msg='.clear() but unset both internal events')

    async def test_cleared_events_are_unset(self):
        # arrange
        e = Event2FA()
        e.set(1)
        e.set(2)

        # act
        e.clear()

        # assert
        assert e.is_set() is False

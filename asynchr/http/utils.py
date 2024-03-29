import threading
from asyncio import current_task
from datetime import datetime


def ts():
    return datetime.now().timestamp()


def tn():
    return threading.current_thread().name


def task_name():
    return current_task().get_name()


def clock():
    return datetime.now().strftime('%H:%M:%S.%f')[:]


def log(what):
    print(f'[{clock()}]: {what}')

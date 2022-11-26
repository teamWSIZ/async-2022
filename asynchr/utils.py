from datetime import datetime


def clock():
    return datetime.now().strftime('%H:%M:%S.%f')[:]


def log(what):
    print(f'[{clock()}]: {what}')
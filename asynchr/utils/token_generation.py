from random import randint
from uuid import uuid4

import numpy as np



def check(size: int):
    have = set()
    for i in range(10 * size):
        token = str(uuid4())[:6]
        # token = randint(0, size - 1)
        if token in have:
            # print(f'duplikat na {i=}')
            return i
        have.add(token)
    return i


if __name__ == '__main__':
    N = 10000
    duplicate_horizon = [check(N) for _ in range(1000)]
    avg = np.average(duplicate_horizon)
    std = np.std(duplicate_horizon)
    median = np.median(duplicate_horizon)
    print(f'Duplikaty dla {N=} średnio po {avg:.1f}+/-{std:.1f} (mediana: {median})')

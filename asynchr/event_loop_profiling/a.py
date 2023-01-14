import random

random.seed(10)

delays = [random.gauss(mu=0, sigma=1) for _ in range(1000)]
print(delays)

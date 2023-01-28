from dataclasses import asdict, dataclass
from random import randint

from locust import task, between, FastHttpUser

"""
Run with:

locust -f loc.py

"""

class QuickstartUser(FastHttpUser):
    wait_time = between(0.001, 0.002)

    @task(5)
    def hello_world(self):
        self.client.get('/')


    # #
    # @task(1)
    # def put_khresults(self):
    #     r = User(0, 'user' + str(randint(0,10**6)), 'Beijing' + str(randint(0,10**6)))
    #     self.client.post('/users', json=asdict(r))

    # @task(1)
    # def post_mid_size_file(self):
    #     url = '/images'
    #     filename = 'mid.bin'
    #     files = {filename: open(filename, 'rb')}
    #     response = self.client.post(url, files=files)

    # def on_start(self):
    #     print('starting')

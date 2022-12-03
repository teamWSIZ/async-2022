from dataclasses import asdict, dataclass
from random import randint

from locust import task, between, FastHttpUser



@dataclass
class User:
    uid: int
    name: str
    address: str


class QuickstartUser(FastHttpUser):
    wait_time = between(0.001, 0.002)

    # @task(5)
    # def hello_world(self):
    #     self.client.get('/welcome?user=Karramba')

    #
    @task(1)
    def put_khresults(self):
        r = User(0, 'user' + str(randint(0,10**6)), 'Beijing' + str(randint(0,10**6)))
        self.client.post('/users', json=asdict(r))

    def on_start(self):
        print('starting')

from nameko.rpc import rpc
from utils import timeout

import time
import random


class GreetingService:
    name = "greetings_service"

    @rpc
    @timeout(5)
    def hello(self, name):
        time.sleep(random.randint(0, 10))
        return "Hello, {}!".format(name)

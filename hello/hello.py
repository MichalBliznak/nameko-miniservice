from nameko.rpc import rpc
from nameko_sentry import SentryReporter
from utils import timeout

import time
import random


class GreetingService:
    name = "greetings_service"
    ID = random.randint(0, 1000)

    sentry = SentryReporter()

    @rpc
    @timeout(2)
    def hello(self, name):
        time.sleep(random.randint(0, 10))
        return "Hello with ID '{}', {}!".format(GreetingService.ID, name)

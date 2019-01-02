from nameko.rpc import rpc
from eventlet import Timeout

import time
import random


class GreetingService:
    name = "greetings_service"

    @rpc
    def hello(self, name):
        timeout = Timeout(5)
        try:
            time.sleep(random.randint(0, 10))
            message = "Hello, {}!".format(name)
        except:
            message = "Ooops, timeout has occurred... :("
        finally:
            timeout.cancel()
        return message

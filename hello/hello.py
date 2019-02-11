from nameko.rpc import rpc
from nameko_sentry import SentryReporter
from nameko.events import BROADCAST, event_handler
from utils import timeout

import time
import random


class GreetingService:
    name = "greetings_service"

    sentry = SentryReporter()

    @rpc
    @timeout(3)
    def hello(self, name):
        time.sleep(random.randint(0, 10))
        return "Hello, {}!".format(name)

    @event_handler("heartbeat_service", "heartbeat", handler_type=BROADCAST, reliable_delivery=False)
    def on_heartbeat(self, ts):
        print("Received Heartbeat with timestamp {}".format(ts), flush=True)

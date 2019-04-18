from nameko.rpc import rpc
from nameko_sentry import SentryReporter
from nameko.events import BROADCAST, event_handler
from utils import timeout

import time
import random
import os
import uuid


class GreetingService:
    name = "greetings_service"

    sentry = SentryReporter()

    uid = uuid.uuid4()

    @rpc
    @timeout(3)
    def hello(self, name):
        time.sleep(random.randint(0, int(os.getenv("RANDOM_TIMEOUT", "0"))))
        return "Hello {}, {} is calling!".format(name, GreetingService.uid)

    @event_handler("heartbeat_service", "heartbeat", handler_type=BROADCAST, reliable_delivery=False)
    def on_heartbeat(self, ts):
        print("Received Heartbeat with timestamp {}".format(ts), flush=True)

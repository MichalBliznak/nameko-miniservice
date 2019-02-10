from nameko.events import EventDispatcher
from nameko.timer import timer
from nameko_sentry import SentryReporter

from datetime import datetime


class HeartbeatService:
    name = "heartbeat_service"

    sentry = SentryReporter()
    dispatch = EventDispatcher()

    @timer(5)
    def send_heartbeat(self):
        timestamp = datetime.now()
        print("Dispatching a heartbeat with timestamp {}".format(timestamp), flush=True)
        self.dispatch("heartbeat", timestamp)

from eventlet import Timeout
from circuitbreaker import circuit


class TimeoutException(Exception):
    pass


def timeout(seconds):
    def timeout_decorator(func):
        @circuit()
        def fcn_wrapper(*args, **kargs):
            with Timeout(seconds, TimeoutException):
                return func(*args, **kargs)

        return fcn_wrapper

    return timeout_decorator

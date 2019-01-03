from eventlet import Timeout


def timeout(seconds):
    def timeout_decorator(func):
        def fcn_wrapper(*args, **kargs):
            t = Timeout(seconds)
            try:
                return func(*args, **kargs)
            except:
                message = "Ooops, timeout has occurred... :("
            finally:
                t.cancel()
            return message

        return fcn_wrapper

    return timeout_decorator

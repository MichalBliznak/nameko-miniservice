from eventlet import Timeout


def timeout(seconds):
    def timeout_decorator(func):
        def fcn_wrapper(*args, **kargs):
            t = Timeout(seconds)
            try:
                return func(*args, **kargs)
            except Timeout:
                message = {"error": {"code": 501, "message": "Service timeout reached"}}
            except Exception as e:
                message = {"error": {"code": 500, "message": "Internal server error: {}".format(e)}}
            finally:
                t.cancel()
            return message

        return fcn_wrapper

    return timeout_decorator

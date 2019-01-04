from flask import request
from redis import Redis
from dynaconf import settings

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY"
    }
}

r = Redis(host=settings["redis_host"], port=settings["redis_port"], db=0)


def authorize(func):
    def check_token(*args, **kargs):
        token = None

        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if token:
            if r.get(token) is not None:
                return func(*args, **kargs)
            else:
                return {"message": "Login needed"}, 403
        else:
            return {"message": "Authorization token is missing"}, 401

    return check_token


def save_token(token, username, expire):
    r.set(token, username)
    r.expire(token, expire)
from flask import request
from redis import Redis
from dynaconf import settings

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY"
    },
    "bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

r = Redis(host=settings["redis_host"], port=settings["redis_port"], db=0)


def authorize(func):
    def check_token(*args, **kargs):
        if "X-API-KEY" in request.headers:
            return check_apikey(*args, **kargs)
        elif "Authorization" in request.headers:
            return check_bearer(*args, **kargs)
        else:
            return {"message": "Authorization token is missing"}, 401

    def check_apikey(*args, **kargs):
        token = request.headers["X-API-KEY"]
        if r.get(token) is not None:
            return func(*args, **kargs)
        else:
            return {"message": "Login is needed"}, 403

    def check_bearer(*args, **kargs):
        token = request.headers["Authorization"]
        token.replace("Bearer ", "")
        if r.get(token) is not None:
            return func(*args, **kargs)
        else:
            return {"message": "Login is needed"}, 403

    return check_token


def save_token(token, username, expire):
    token.replace("Bearer ", "")
    r.set(token, username)
    r.expire(token, expire)


def delete_token():
    token = None
    if "X-API-KEY" in request.headers:
        token = request.headers["X-API-KEY"]
    elif "Authorization" in request.headers:
        token = request.headers["Authorization"].replace("Bearer ", "")
    r.delete(token)

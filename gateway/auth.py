from flask import request
from redis import Redis
from dynaconf import settings
from errors import error

import jwt

authorizations = {
    "bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

# Initialize Redis
r = Redis(host=settings["redis_host"], port=settings["redis_port"], db=0)

# Initialize the auth secret
secret = settings["JWT_SECRET"]


def authorize(func):
    def check_token(*args, **kargs):
        try:
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].replace("Bearer ", "")
                payload = jwt.decode(token, secret, algorithms="HS256")
                t = r.get(payload["userId"])
                if t is not None and t.decode() == payload["token"]:
                    return func(*args, **kargs)
                else:
                    return {"message": "Login is needed"}, 403
            else:
                return {"message": "Authorization token is missing"}, 401
        except Exception as e:
            return {"error": error(500, "Unable to authorize the request: {}".format(e))}

    return check_token


def save_token(token, expire):
    payload = jwt.decode(token, secret, algorithms="HS256")
    r.set(payload["userId"], payload["token"])
    r.expire(payload["userId"], expire)


def delete_token():
    token = request.headers["Authorization"].replace("Bearer ", "")
    payload = jwt.decode(token, secret, algorithms="HS256")
    r.delete(payload["userId"])


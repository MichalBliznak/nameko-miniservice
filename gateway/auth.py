from flask import request

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY"
    }
}


def authorize(call):
    def check_token(*args, **kargs):
        token = None

        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if token:
            if token == "1234":
                return call(*args, **kargs)
            else:
                return {"message": "Forbidden"}, 403
        else:
            return {"message": "Authorization token is missing"}, 401

    return check_token

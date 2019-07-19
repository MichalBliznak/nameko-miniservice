from flask import request
from flask_restplus import Resource, fields, Namespace
from core.errors import error
from core.nameko import rpc
from core.limiter import limiter
from security.auth import authorize, save_token, delete_token
from dynaconf import settings

api = Namespace("login", description="Login API")

# Set up models
login_model = api.model('Login', {
    'username': fields.String(required=True, description='User name'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/')
class LoginController(Resource):
    decorators = [limiter.limit(settings["limit_login"])]

    @api.doc(responses={403: "Forbidden", 429: "Too many requests", 200: "OK", 500: "Internal server error"})
    @api.expect(login_model)
    def post(self):
        try:
            payload = request.json
            res = rpc.auth_service.login(payload["username"], payload["password"])
            if "access_token" in res.keys():
                save_token(res["access_token"], settings["token_expiration"])
                return {"status": "Success",
                        "access_token": res["access_token"]}
            else:
                raise Exception("Unknown response format")
        except Exception as e:
            return {"status": "Unable to login",
                    "error": error(403, "Forbidden: {}".format(e))}, 403

    @api.doc(security="bearer")
    @api.doc(responses={429: "Too many requests", 200: "OK", 500: "Internal server error"})
    @authorize
    def delete(self):
        try:
            delete_token()
            return {"status": "Success"}
        except Exception as e:
            return {"status": "Unable to logout",
                    "error": error(500, "Internal server error: {}".format(e))}, 500

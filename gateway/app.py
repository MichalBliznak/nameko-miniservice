#!/usr/bin/env python3

from flask import Flask, request
from flask_nameko import FlaskPooledClusterRpcProxy
from flask_restplus import Resource, Api, fields
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from auth import authorize, authorizations, save_token, delete_token
from errors import error
from dynaconf import settings

# Flask setup
app = Flask(__name__)
app.config.update(dict(NAMEKO_AMQP_URI=settings["rabbit_uri"],
                       NAMEKO_POOL_RECYCLE=settings["pool_recycle"]))

# Flask RESTplus setup
api = Api(app, version='1.0', title='Hello Cloud API',
          description='A sample cloud project demonstrating Flask + Nameko frameworks',
          authorizations=authorizations)

# Flask Limiter setup
limiter = Limiter(app, key_func=get_remote_address)

ns_login = api.namespace("login", description="Login API")
ns_api = api.namespace("api", description="Features API")

# Nameko setup
rpc = FlaskPooledClusterRpcProxy()
rpc.init_app(app)

# Set up models
login_model = api.model('Login', {
    'username': fields.String(required=True, description='User name'),
    'password': fields.String(required=True, description='User password')
})


@ns_api.route('/hello/<name>')
class HelloController(Resource):
    decorators = [limiter.limit(settings["limit_api"])]
    @api.doc(params={'name': 'Name to say Hello'})
    @api.doc(security="bearer")
    @api.doc(responses={401: "Not Authorized", 403: "Forbidden", 429: "Too many requests", 200: "OK", 500: "Internal server error"})
    @authorize
    def get(self, name):
        try:
            message = rpc.greetings_service.hello(name)
            return {"message": message}
        except Exception as e:
            return {"error": error(500, "Internal server error: {}".format(e))}, 500


@ns_login.route('/')
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
    @limiter.limit(settings["limit_login"])
    @authorize
    def delete(self):
        try:
            delete_token()
            return {"status": "Success"}
        except Exception as e:
            return {"status": "Unable to logout",
                    "error": error(500, "Internal server error: {}".format(e))}, 500


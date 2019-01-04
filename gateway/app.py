#!/usr/bin/env python3

from flask import Flask, request
from flask_nameko import FlaskPooledClusterRpcProxy
from flask_restplus import Resource, Api, fields

from auth import authorize, authorizations

from dynaconf import settings

# Flask setup
app = Flask(__name__)
app.config.update(dict(NAMEKO_AMQP_URI=settings["rabbit_host"]))

# Flask RESTplus setup
api = Api(app, version='1.0', title='Hello Cloud API',
          description='A sample cloud project demonstrating Flask + Nameko frameworks',
          authorizations=authorizations)

ns_login = api.namespace("login", description="Login API")
ns_api = api.namespace("api", description="Features API")

# Nameko setup
rpc = FlaskPooledClusterRpcProxy()
rpc.init_app(app)

# Set up models
login_model = api.model('Login', {
    'user': fields.String(required=True, description='User name'),
    'password': fields.String(required=True, description='User password')
})


@ns_api.route('/hello/<name>')
class HelloController(Resource):
    @api.doc(params={'name': 'Name to say Hello'})
    @api.doc(security="apikey")
    @api.doc(responses={401: "Not Authorized", 403: "Forbidden", 200: "OK"})
    @authorize
    def get(self, name):
        try:
            message = rpc.greetings_service.hello(name)
        except:
            message = "Ooops, the service seems to be unreachable... :("
        return {"message": message}


@ns_login.route('/')
class LoginController(Resource):
    @api.doc(responses={403: "Forbidden", 200: "OK"})
    @api.expect(login_model)
    def post(self):
        payload = request.json
        return {"message": "Not implemented yet"}

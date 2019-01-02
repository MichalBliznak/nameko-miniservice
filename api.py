#!/usr/bin/env python3

from flask import Flask
from flask_nameko import FlaskPooledClusterRpcProxy
from flask_restplus import Resource, Api
from auth import authorize, authorizations

# Flask setup
app = Flask(__name__)
app.config.update(dict(NAMEKO_AMQP_URI='amqp://localhost'))

# Flask RESTplus setup

api = Api(app, version='1.0', title='Sample API', description='A sample API', authorizations=authorizations)

# Nameko setup
rpc = FlaskPooledClusterRpcProxy()
rpc.init_app(app)


@api.route('/hello/<name>')
class HelloController(Resource):
    @api.doc(params={'name': 'Name to say Hello'})
    @api.doc(security="apikey")
    @api.doc(responses={401: "Not Authorized", 403: "Forbidden", 200: "OK"})
    @authorize
    def get(self, name):
        res = rpc.greetings_service.hello.call_async(name)
        return {"message": res.result()}

#!/usr/bin/env python3

from flask import Flask
from flask_restplus import Api
from security.auth import authorizations
from apis.api import api as ns_api
from apis.auth import api as ns_login
from core.nameko import rpc
from core.limiter import limiter
from dynaconf import settings

# Flask setup
app = Flask(__name__)
app.config.update(dict(NAMEKO_AMQP_URI=settings["rabbit_uri"],
                       NAMEKO_POOL_RECYCLE=settings["pool_recycle"]))

# Flask RESTplus setup
api = Api(app, version='1.0', title='Hello Cloud API',
          description='A sample cloud project demonstrating Flask + Nameko frameworks',
          authorizations=authorizations,
          doc='/swagger/')

api.add_namespace(ns_login)
api.add_namespace(ns_api)

# Flask Limiter setup
limiter.init_app(app)

# Nameko setup
rpc.init_app(app)

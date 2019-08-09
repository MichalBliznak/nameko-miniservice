from flask import Blueprint
from flask_restplus import Api
from security.auth import authorizations
from apis.api import api as ns_api
from apis.auth import api as ns_login

blueprint = Blueprint('api', __name__, url_prefix='/api/1')

# Flask RESTplus setup
api = Api(blueprint, version='1.0', title='Hello Cloud API',
          description='A sample cloud project demonstrating Flask + Nameko frameworks',
          authorizations=authorizations,
          doc='/swagger/')

api.add_namespace(ns_login, path="/login")
api.add_namespace(ns_api, path="")

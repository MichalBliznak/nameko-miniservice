from flask_restplus import Resource, Namespace
from core.errors import error
from core.limiter import limiter
from core.nameko import rpc
from security.auth import authorize
from dynaconf import settings

api = Namespace("api", description="Features API")


@api.route('/hello/<name>')
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



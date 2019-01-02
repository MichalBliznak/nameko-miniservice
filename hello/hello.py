from nameko.rpc import rpc


class GreetingService:
    name = "greetings_service"

    @rpc
    def hello(self, name):
        return "Hello, {}!".format(name)

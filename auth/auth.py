from nameko.rpc import rpc
from utils import timeout


class LoginService:
    name = "auth_service"

    @rpc
    @timeout(3)
    def login(self, username, password):
        return {"access_token": "1234"}

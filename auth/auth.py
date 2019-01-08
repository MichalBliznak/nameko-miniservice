from nameko.rpc import rpc
from utils import timeout
from models import User, Base
from nameko_sqlalchemy import Database
from sqlalchemy.orm.exc import NoResultFound

import random
import base64


class LoginService:
    name = "auth_service"

    db = Database(Base)

    @staticmethod
    def create_token():
        arr = bytearray(32)
        for i in range(0, 32):
            arr[i] = random.randint(0, 255)
        return base64.encodebytes(arr).decode().rstrip()

    @rpc
    @timeout(3)
    def login(self, username, password):
        try:
            pswd = self.db.get_session().query(User).filter(User.username == username).one().password
            if password == pswd:
                return {"access_token": self.create_token()}
            else:
                raise NoResultFound()
        except NoResultFound:
            return {"error": {"code": 403, "message": "Invalid credentials"}}

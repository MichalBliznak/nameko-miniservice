from nameko.rpc import rpc
from utils import timeout
from models import User, Base
from nameko_sqlalchemy import Database
from nameko_sentry import SentryReporter
from sqlalchemy.orm.exc import NoResultFound

import random
import base64
import jwt


class LoginService:
    name = "auth_service"
    secret = "aYoXW26E7w3wiVOq4TnHGEkx0OB4cdHx"

    db = Database(Base)
    sentry = SentryReporter()

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
            rec = self.db.get_session().query(User).filter(User.username == username).one()
            if password == rec.password:
                payload = {"userId": rec.userid,
                           "token": self.create_token()}
                return {"access_token": jwt.encode(payload, self.secret, algorithm="HS256").decode().rstrip()}
            else:
                raise NoResultFound()
        except NoResultFound:
            return {"error": {"code": 403, "message": "Invalid credentials"}}

from nameko.rpc import rpc
from utils import timeout
from models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

import random
import base64


engine = create_engine('sqlite:///credentials.sqlite')
Session = sessionmaker(bind=engine)
db_session = Session()


class LoginService:
    name = "auth_service"

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
            pswd = db_session.query(User).filter(User.username == username).one().password
            if password == pswd:
                return {"access_token": self.create_token()}
            else:
                raise NoResultFound()
        except NoResultFound:
            return {"error": {"code": 403, "message": "Invalid credentials"}}

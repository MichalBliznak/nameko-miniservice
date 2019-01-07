from nameko.rpc import rpc
from utils import timeout
from models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///credentials.sqlite')
Session = sessionmaker(bind=engine)
db_session = Session()


class LoginService:
    name = "auth_service"

    @rpc
    @timeout(3)
    def login(self, username, password):
        #passwd = db_session.query(User).filter(User.username.match(username)).one().password
        passwd = "7706034204"
        if password == passwd:
            return {"access_token": "1234"}
        else:
            return {}

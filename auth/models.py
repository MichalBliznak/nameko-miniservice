from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"
    userid = Column(String, primary_key=True)
    username = Column(String)
    password = Column(String)

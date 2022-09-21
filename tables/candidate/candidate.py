from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from engine.engine import MAIN_ENGINE

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer, primary_key=True, unique=True)
    firebase_id = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    email = Column(String(100), unique=True)
    country = Column(String)
    zone = Column(String)
    phone_number = Column(String)

    def __init__(
        self,
        firebase_id,
        username,
        password,
        email,
        country=None,
        zone=None,
        phone_number=None,
    ):
        self.firebase_id = firebase_id
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.zone = zone
        self.phone_number = phone_number


def create():
    Base.metadata.create_all(MAIN_ENGINE)

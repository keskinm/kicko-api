from sqlalchemy import Column, Integer, String

from engine.base import Base
from engine.engine import MAIN_ENGINE


class Professional(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    firebase_id = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    email = Column(String(100), unique=True)
    country = Column(String)
    zone = Column(String)
    phone_number = Column(String)

    language = Column(String)

    def __init__(
        self,
        firebase_id,
        username,
        password,
        email,
        country=None,
        zone=None,
        phone_number=None,
        language="french",
    ):
        self.firebase_id = firebase_id
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.zone = zone
        self.phone_number = phone_number

        self.language = language


def create():
    Base.metadata.create_all(MAIN_ENGINE)

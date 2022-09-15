from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from engine.engine import MAIN_ENGINE

from tables.professional.user import User

Base = declarative_base()


class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey(User.id))
    email = Column(String(100), unique=True)
    country = Column(String)
    city = Column(String)
    phone_number = Column(String)

    def __init__(
        self,
        user_id,
        email=None,
        country=None,
        city=None,
        phone_number=None,
    ):
        self.user_id = user_id
        self.email = email
        self.country = country
        self.city = city
        self.phone_number = phone_number


Base.metadata.create_all(MAIN_ENGINE)

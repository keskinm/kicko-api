from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from engine.engine import MAIN_ENGINE
from tables.professional.user import User

Base = declarative_base()


class JobOffers(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    description = Column(String)
    requires = Column(String)

    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, name, description, requires, user_id):
        self.name = name
        self.description = description
        self.requires = requires
        self.user_id = user_id


Base.metadata.create_all(MAIN_ENGINE)

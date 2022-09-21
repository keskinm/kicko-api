from sqlalchemy import Column, Integer, String, ForeignKey

from engine.base import Base
from engine.engine import MAIN_ENGINE
from tables.professional.professional import Professional


class JobOffers(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    description = Column(String)
    requires = Column(String)

    business_id = Column(Integer, ForeignKey(Professional.id))

    def __init__(self, name, description, requires, business_id):
        self.name = name
        self.description = description
        self.requires = requires
        self.business_id = business_id


def create():
    Base.metadata.create_all(MAIN_ENGINE)

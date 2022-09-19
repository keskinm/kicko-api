from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from engine.engine import MAIN_ENGINE
from tables.professional.professional import Professional

Base = declarative_base()


class JobOffers(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    description = Column(String)
    requires = Column(String)

    professional_id = Column(Integer, ForeignKey(Professional.id))

    def __init__(self, name, description, requires, professional_id):
        self.name = name
        self.description = description
        self.requires = requires
        self.professional_id = professional_id


Base.metadata.create_all(MAIN_ENGINE)

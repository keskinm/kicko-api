from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from engine.base import Base

from engine.engine import MAIN_ENGINE
from tables.associations.associations import job_offer_candidate_association


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

    job_offers = relationship(
        "JobOffers",
        secondary=job_offer_candidate_association,
        back_populates="candidate",
    )

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

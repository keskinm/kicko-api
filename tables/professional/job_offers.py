from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from engine.base import Base
from engine.engine import MAIN_ENGINE
from tables.associations.associations import job_offer_candidate_association
from tables.professional.professional import Professional


class JobOffers(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    description = Column(String)
    requires = Column(String)

    business_id = Column(Integer, ForeignKey(Professional.id))

    # @todo rename candidate -> candidates wherever need
    candidate = relationship(
        "Candidate",
        secondary=job_offer_candidate_association,
        back_populates="job_offers",
    )

    def __init__(self, name, description, requires, business_id):
        self.name = name
        self.description = description
        self.requires = requires
        self.business_id = business_id


def create():
    from tables.candidate.candidate import Candidate

    Base.metadata.create_all(MAIN_ENGINE)

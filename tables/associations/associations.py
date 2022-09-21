from sqlalchemy import Table, Column, ForeignKey, Integer

from engine.base import Base
from engine.engine import MAIN_ENGINE

job_offer_candidate_association = Table(
    "job_offer_candidate_association",
    Base.metadata,
    Column("job_offer_id", Integer, ForeignKey("job_offers.class_id")),
    Column("candidate_id", Integer, ForeignKey("candidate.user_id")),
)


def create():
    Base.metadata.create_all(MAIN_ENGINE)

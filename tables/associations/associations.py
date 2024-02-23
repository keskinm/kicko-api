from sqlalchemy import Column, ForeignKey, Integer, Table

from engine.base import Base

# @todo Gather all tables in one file.

job_offer_candidate_association = Table(
    "job_offer_candidate_association",
    Base.metadata,
    Column("job_offer_id", Integer, ForeignKey("job_offers.id")),
    Column("candidate_id", Integer, ForeignKey("candidate.id")),
)

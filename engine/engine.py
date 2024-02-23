from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from engine.base import Base

DATABASE_URL = "sqlite:///main_engine.db"
MAIN_ENGINE = create_engine(DATABASE_URL, echo=True)


if __name__ == "__main__":
    from tables import (
        Candidate,
        Business,
        JobOffers,
        Professional,
        job_offer_candidate_association,
    )

    Base.metadata.create_all(MAIN_ENGINE)

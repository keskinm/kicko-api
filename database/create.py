from database.database import MAIN_ENGINE
from database.base import Base


if __name__ == "__main__":
    from tables import (
        Candidate,
        Business,
        JobOffers,
        Professional,
        job_offer_candidate_association,
    )

    Base.metadata.create_all(MAIN_ENGINE)

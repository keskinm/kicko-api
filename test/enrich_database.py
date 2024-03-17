"""Module to enrich a mock/test database with objects."""

from models.candidate.candidate import Candidate
from models.professional.professional import Professional


def fill_db_with_users(app):
    """Fill database with a Candidate instance."""
    app.db_session.add(
        Candidate(
            firebase_id="1234",
            username="toto",
            password="toto",
            email="toto@gmail.com",
            country="France",
            zone="",
            phone_number="070000000",
        )
    )
    app.db_session.add(
        Professional(
            firebase_id="12345",
            username="professional",
            password="professional",
            email="professional@gmail.com",
            country="France",
            zone="",
            phone_number="070000000",
        )
    )
    app.db_session.commit()

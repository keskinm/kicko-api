"""Module to enrich a mock/test database with objects."""

from models.candidate.candidate import Candidate
from models.professional.professional import Professional
from models.professional.business import Business
from models.professional.job_offers import JobOffers



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


def fill_db_with_business(app):
    fill_db_with_users(app)
    pro_id = app.db_session.query(Professional).first().id
    app.db_session.add(
        Business(
            professional_id=pro_id
        )
    )
    app.db_session.commit()


def fill_db_with_job_offers_and_appliers(app):
    fill_db_with_business(app)
    business_id = app.db_session.query(Business).first().id
    app.db_session.add(
        JobOffers(
            name="12345",
            description="professional",
            requires="professional",
            business_id=business_id,
        )
    )
    app.db_session.commit()

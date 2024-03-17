import os
import sys
from unittest import mock
import pytest
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import scoped_session, sessionmaker

from api.base import register_instance_methods
from api.controllers_factory import controllers
from app import app
from database.base import Base
from models.candidate.candidate import Candidate as mCandidate
from models.professional.professional import Professional as mProfessional
from models.professional.business import Business as mBusiness
from models.professional.job_offers import JobOffers as mJobOffers
from settings import TestSettings


TestSettings(app)


@pytest.fixture(scope="function")
def test_client():
    app.config["TESTING"] = True
    app.config["DATABASE_URL"] = "sqlite:///test_database.db"

    test_engine = create_engine(app.config["DATABASE_URL"], echo=True)
    Base.metadata.create_all(test_engine)
    app.db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    )

    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    try:
        with mock.patch("api.common.SessionLocal", app.db_session):
            yield testing_client
    finally:
        ctx.pop()
        Base.metadata.drop_all(test_engine)
        app.db_session.remove()
        test_engine.dispose()


@pytest.fixture(scope="function")
def with_users_test_client(test_client):
    """Fill database with a two users: one candidate and a pro."""
    app.db_session.add(
        mCandidate(
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
        mProfessional(
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
    yield test_client


@pytest.fixture(scope="function")
def fill_db_with_business(with_users_test_client):
    pro_id = app.db_session.query(Professional).first().id
    app.db_session.add(Business(professional_id=pro_id))
    app.db_session.commit()
    yield with_users_test_client


@pytest.fixture(scope="function")
def fill_db_with_job_offers_and_appliers(fill_db_with_business):
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
    yield fill_db_with_business

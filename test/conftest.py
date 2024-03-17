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

for controller in controllers:
    register_instance_methods(app, controller())


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
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=test_engine
        )
        with mock.patch("api.common.SessionLocal", TestingSessionLocal):
            yield testing_client
    finally:
        ctx.pop()
        Base.metadata.drop_all(test_engine)
        app.db_session.remove()
        test_engine.dispose()


def fill_db_with_candidate(app):
    """Fill database with a Candidate instance."""
    obj = mCandidate(
        firebase_id="1234",
        username="toto",
        password="toto",
        email="toto@gmail.com",
        country="France",
        zone="",
        phone_number="070000000",
    )
    app.db_session.add(obj)
    app.db_session.commit()


@pytest.fixture(scope="function")
def filled_db_test_client(test_client):
    fill_db_with_candidate(app)
    yield test_client

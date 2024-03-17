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

from test.enrich_database import fill_db_with_users


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
        with mock.patch("api.common.SessionLocal", app.db_session):
            yield testing_client
    finally:
        ctx.pop()
        Base.metadata.drop_all(test_engine)
        app.db_session.remove()
        test_engine.dispose()


@pytest.fixture(scope="function")
def filled_db_test_client(test_client):
    fill_db_with_users(app)
    yield test_client

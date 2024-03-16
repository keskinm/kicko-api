import pytest
from app import app
from database.base import Base
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = "sqlite:///test_database.db"

    test_engine = create_engine(app.config['DATABASE_URL'], echo=True)
    # from tables import tables_importer
    #@todo RENOMMER "tables" en "models"
    Base.metadata.create_all(test_engine)
    app.db_session = scoped_session(sessionmaker(autocommit=False,
                                                  autoflush=False,
                                                  bind=test_engine))

    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

def test_delete_candidate_account(test_client):
    response = test_client.get('/api/delete_candidate_account', headers={"Authorization": "Bearer token"})
    assert response.status_code == 200


# def test_delete_candidate_account_with_valid_token():
#     valid_auth_header = 'Bearer valid_token'
#     response = self.client.get(
#         "/api/delete_candidate_account",
#         headers={"Authorization": valid_auth_header}
#     )
#     self.assertEqual(response.status_code, 200)
#     data = json.loads(response.data)
#     self.assertEqual(data['status'], 'success')
#
# def test_delete_candidate_account_with_invalid_token():
#     invalid_auth_header = 'Bearer invalid_token'
#     response = self.client.get(
#         "/api/delete_candidate_account",
#         headers={"Authorization": invalid_auth_header}
#     )
#     self.assertEqual(response.status_code, 401)
#     data = json.loads(response.data)
#     self.assertEqual(data['status'], 'fail')

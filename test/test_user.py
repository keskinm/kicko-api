import json
from unittest import mock
from app import app
import pytest
from models.candidate.candidate import Candidate as mCandidate
from models.professional.professional import Professional as mProfessional


@pytest.mark.parametrize(
    "table, auth_header, expc_status_code, expc_status",
    [
        (mCandidate, {"Authorization": "Bearer faux_token_valide"}, 200, "success"),
        (mProfessional, {"Authorization": "Bearer faux_token_valide"}, 200, "success"),
        (mCandidate, None, 401, "fail"),
        (mProfessional, None, 401, "fail"),
    ],
)
def test_delete_user_account(
    filled_db_test_client, table, auth_header, expc_status_code, expc_status
):
    email = app.db_session.query(table).first().email
    with mock.patch("api.user.User.decode_auth_token") as mock_decode:
        mock_decode.return_value = (True, email)

        response = filled_db_test_client.get(
            f"/api/delete_user_account/{table.__name__.lower()}",
            headers=auth_header,
        )
        assert response.status_code == expc_status_code
        data = json.loads(response.data)
        assert data["status"] == expc_status
        users = app.db_session.query(table).filter()
        if expc_status_code == 200:
            assert users.count() == 0
        else:
            assert users.count() == 1

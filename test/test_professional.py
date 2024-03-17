import json
from unittest import mock
from app import app
import pytest
from models.candidate.candidate import Candidate as mCandidate


@pytest.mark.parametrize(
    "auth_header, expc_status_code, expc_status",
    [
        ({"Authorization": "Bearer faux_token_valide"}, 200, "success"),
        (None, 401, "fail"),
    ],
)
def test_delete_candidate_account(
    filled_db_test_client, auth_header, expc_status_code, expc_status
):
    with mock.patch("api.common.decode_auth_token") as mock_decode:
        mock_decode.return_value = (True, "toto@gmail.com")

        response = filled_db_test_client.get(
            "/api/delete_candidate_account",
            headers=auth_header,
        )
        assert response.status_code == expc_status_code
        data = json.loads(response.data)
        assert data["status"] == expc_status
        users = app.db_session.query(mCandidate).filter()
        if expc_status_code == 200:
            assert users.count() == 0
        else:
            assert users.count() == 1

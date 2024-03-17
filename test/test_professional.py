import json
from unittest import mock

import pytest


@pytest.mark.parametrize(
    "auth_header, expc_status_code, expc_status",
    [
        ({"Authorization": "Bearer faux_token_valide"}, 200, "success"),
        (None, 401, "fail"),
    ],
)
def test_delete_candidate_account(
    test_client, auth_header, expc_status_code, expc_status
):
    with mock.patch("api.common.decode_auth_token") as mock_decode:
        mock_decode.return_value = (True, "toto@gmail.com")

        response = test_client.get(
            "/api/delete_candidate_account",
            headers=auth_header,
        )
        assert response.status_code == expc_status_code
        data = json.loads(response.data)
        assert data["status"] == expc_status

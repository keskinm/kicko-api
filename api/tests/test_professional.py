import json
from unittest import mock

import pytest


def test_delete_candidate_account(test_client):
    with mock.patch("api.common.decode_auth_token") as mock_decode:
        mock_decode.return_value = (True, "email@example.com")

        response = test_client.get(
            "/api/delete_candidate_account",
            headers={"Authorization": "Bearer faux_token_valide"},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"

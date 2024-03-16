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

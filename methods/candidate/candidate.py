from methods.base import Methods
from flask import request, jsonify

from methods.common import (
    get_token,
    add_row,
    get_user,
)
from tables.candidate.candidate import Candidate as TCandidate


class Candidate(Methods):
    def __init__(self, app):
        post_methods = [self.candidate_authentication_token, self.candidate_register]

        get_methods = [self.candidate]

        Methods.__init__(
            self, app=app, post_methods=post_methods, get_methods=get_methods
        )

    def candidate(self):
        auth_header = request.headers.get("Authorization")
        return get_user(table=TCandidate, auth_header=auth_header, app=self.app)

    def candidate_authentication_token(self):
        input_json = request.get_json(force=True)
        return get_token(table=TCandidate, input_json=input_json, app=self.app)

    def candidate_register(self):
        input_json = request.get_json(force=True)
        add_row(TCandidate, input_json)
        resp = jsonify({})
        resp.status_code = 200
        return resp

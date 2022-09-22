from methods.base import Methods
from flask import request, jsonify

from methods.common import (
    make_query,
    row_to_dict,
    get_token,
    add_row,
    get_user,
)
from tables.professional.business import Business as TBusiness
from tables.professional.professional import Professional as TProfessional


class Professional(Methods):
    def __init__(self, app):
        post_methods = [
            self.professional_authentication_token,
            self.professional_register,
        ]

        get_methods = [self.professional]

        Methods.__init__(
            self, app=app, post_methods=post_methods, get_methods=get_methods
        )

    def professional(self):
        auth_header = request.headers.get("Authorization")
        return get_user(table=TProfessional, auth_header=auth_header, app=self.app)

    def professional_authentication_token(self):
        input_json = request.get_json(force=True)
        return get_token(table=TProfessional, input_json=input_json, app=self.app)

    def professional_register(self):
        input_json = request.get_json(force=True)
        add_row(TProfessional, input_json)
        professional_id = row_to_dict(
            make_query(
                TProfessional, TProfessional.email == input_json["email"]
            ).first()
        )
        add_row(TBusiness, {"professional_id": professional_id["id"]})
        resp = jsonify({})
        resp.status_code = 200
        return resp

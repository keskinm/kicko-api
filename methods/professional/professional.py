from flask import jsonify, request

from methods.base import Methods
from methods.common import (
    add_row,
    get_token,
    get_user,
    make_query,
    row_to_dict,
    delete_user,
)
from tables.professional.business import Business as TBusiness
from tables.professional.professional import Professional as TProfessional


class Professional(Methods):
    def __init__(self):
        post_methods = [
            self.professional_authentication_token,
            self.professional_register,
        ]

        get_methods = [self.professional, self.delete_professional_account]

        Methods.__init__(self, post_methods=post_methods, get_methods=get_methods)

    def professional(self):
        auth_header = request.headers.get("Authorization")
        return get_user(table=TProfessional, auth_header=auth_header)

    def delete_professional_account(self):
        auth_header = request.headers.get("Authorization")
        return delete_user(table=TProfessional, auth_header=auth_header)

    def professional_authentication_token(self):
        input_json = request.get_json(force=True)
        return get_token(table=TProfessional, input_json=input_json)

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

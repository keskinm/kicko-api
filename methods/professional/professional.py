from flask import jsonify, request

from methods.base import Methods
from methods.common import (add_row, delete_user, get_token, get_user,
                            make_query, row_to_dict)
from tables.professional.business import Business as TBusiness
from tables.professional.professional import Professional as TProfessional
from app import app


class Professional(Methods):
    @staticmethod
    @app.route("/api/professional", methods=["GET"])
    def professional():
        auth_header = request.headers.get("Authorization")
        return get_user(table=TProfessional, auth_header=auth_header)

    @staticmethod
    @app.route("/api/delete_professional_account", methods=["GET"])
    def delete_professional_account():
        auth_header = request.headers.get("Authorization")
        return delete_user(table=TProfessional, auth_header=auth_header)

    @staticmethod
    @app.route("/api/professional_authentication_token", methods=["POST"])
    def professional_authentication_token():
        input_json = request.get_json(force=True)
        return get_token(table=TProfessional, input_json=input_json)

    @staticmethod
    @app.route("/api/professional_register", methods=["POST"])
    def professional_register():
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

from flask import jsonify, request

from api.common import add_row, make_query, row_to_dict
from api.user import User
from app import app
from models.professional.business import Business as TBusiness
from models.professional.professional import Professional as TProfessional


class Professional(User):
    """Professional User."""

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

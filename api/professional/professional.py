from flask import jsonify, request

from api.base import instance_method_route
from api.common import add_row, make_query, row_to_dict
from api.user import User
from app import app
from models.professional.business import Business as TBusiness
from models.professional.professional import Professional as TProfessional


class Professional(User):
    """Professional User."""

    @staticmethod
    def replace(session, table_row, fields):
        for key, value in fields.items():
            setattr(table_row, key, value)
        session.commit()
        session.close()

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

    @instance_method_route("professional_update_profile/<professional_id>", methods=["POST"])
    def professional_update_profile(self, professional_id):
        input_json = request.get_json(force=True)
        query, session = make_query(
            TProfessional, TProfessional.id == professional_id, end_session=False
        )
        self.replace(session, query.first(), input_json)
        result = jsonify({"success": True})
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/professional_get_profile/<pro_id>", methods=["GET"])
    def professional_get_profile(pro_id):
        pro = row_to_dict(
            make_query(TProfessional, TProfessional.id == pro_id).one()
        )
        result = jsonify(pro)
        result.status_code = 200
        return result

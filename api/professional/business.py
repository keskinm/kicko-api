from flask import jsonify, request

from app import app
from api.base import ApiController
from api.common import make_query, replace, row_to_dict
from tables.professional.business import Business as TBusiness


class Business(ApiController):
    @staticmethod
    @app.route("/api/get_business/<professional_id>", methods=["GET"])
    def get_business(professional_id):
        result = row_to_dict(
            make_query(TBusiness, TBusiness.professional_id == professional_id).first()
        )
        result = jsonify(result)
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/update_business_fields/<professional_id>", methods=["POST"])
    def update_business_fields(professional_id):
        input_json = request.get_json(force=True)
        query, session = make_query(
            TBusiness, TBusiness.professional_id == professional_id, end_session=False
        )
        replace(session, query.first(), input_json)
        result = jsonify({"success": True})
        result.status_code = 200
        return result

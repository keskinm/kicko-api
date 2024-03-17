from flask import jsonify, request

from api.base import instance_method_route
from api.common import add_row, make_query, row_to_dict
from api.user import User
from app import app
from models.candidate.candidate import Candidate as TCandidate
from models.candidate.candidate import enums_to_module, enums_values


class Candidate(User):
    """Candidate User."""

    def __init__(self):
        super().__init__()
        self.enums_set_attr = {
            "sex": self.set_attr_enum,
            "study_level": self.set_attr_enum,
        }

    @staticmethod
    def set_attr_enum(table_row, key, value):
        value = enums_to_module[key](value)
        setattr(table_row, key, value)

    def replace(self, session, table_row, fields):
        for key, value in fields.items():
            if key in self.enums_set_attr:
                self.enums_set_attr[key](table_row, key, value)
            else:
                setattr(table_row, key, value)
        session.commit()
        session.close()

    @instance_method_route("candidate_update_profile/<candidate_id>", methods=["POST"])
    def candidate_update_profile(self, candidate_id):
        input_json = request.get_json(force=True)
        query, session = make_query(
            TCandidate, TCandidate.id == candidate_id, end_session=False
        )
        self.replace(session, query.first(), input_json)
        result = jsonify({"success": True})
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/get_candidate_syntax", methods=["GET"])
    def get_candidate_syntax():
        result = jsonify(enums_values)
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/candidate_get_profile/<candidate_id>", methods=["GET"])
    def candidate_get_profile(candidate_id):
        candidate = row_to_dict(
            make_query(TCandidate, TCandidate.id == candidate_id).one()
        )
        result = jsonify(candidate)
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/candidate_register", methods=["POST"])
    def candidate_register():
        input_json = request.get_json(force=True)
        add_row(TCandidate, input_json)
        resp = jsonify({})
        resp.status_code = 200
        return resp

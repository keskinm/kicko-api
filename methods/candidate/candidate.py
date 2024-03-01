from flask import jsonify, request

from app import app
from methods.base import Methods, instance_method_route
from methods.common import (add_row, delete_user, get_token, get_user,
                            make_query, row_to_dict)
from tables.candidate.candidate import Candidate as TCandidate
from tables.candidate.candidate import candidate_syntax, enums_to_module


class Candidate(Methods):
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

    @instance_method_route("get_candidate_syntax/<user_id>", methods=["POST"])
    def get_candidate_syntax(self, user_id):
        input_json = request.get_json(force=True)
        q_user_group = input_json["user_group"]
        table = self.table_routes["user_group"][q_user_group]
        id_attr = table.id
        # id_attr = getattr(table, id)

        user = row_to_dict(make_query(table, id_attr == user_id).one())

        result = jsonify(candidate_syntax[user["language"]])
        result.status_code = 200
        print("result ici", candidate_syntax[user["language"]])
        return result

    @staticmethod
    @app.route("/api/candidate_get_profile/<candidate_id>", methods=["GET"])
    def candidate_get_profile(candidate_id):
        candidate = row_to_dict(
            make_query(TCandidate, TCandidate.id == candidate_id).one()
        )

        # @todo delete syntax here and use get_candidate_syntax instead?
        result = jsonify(
            {"instance": candidate, "syntax": candidate_syntax[candidate["language"]]}
        )
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/candidate", methods=["GET"])
    def candidate():
        auth_header = request.headers.get("Authorization")
        return get_user(table=TCandidate, auth_header=auth_header)

    @staticmethod
    @app.route("/api/delete_candidate_account", methods=["GET"])
    def delete_candidate_account():
        auth_header = request.headers.get("Authorization")
        return delete_user(table=TCandidate, auth_header=auth_header)

    @staticmethod
    @app.route("/api/candidate_authentication_token", methods=["POST"])
    def candidate_authentication_token():
        input_json = request.get_json(force=True)
        return get_token(table=TCandidate, input_json=input_json)

    @staticmethod
    @app.route("/api/candidate_register", methods=["POST"])
    def candidate_register():
        input_json = request.get_json(force=True)
        add_row(TCandidate, input_json)
        resp = jsonify({})
        resp.status_code = 200
        return resp

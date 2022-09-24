from methods.base import Methods
from flask import request, jsonify

from methods.common import (
    get_token,
    add_row,
    get_user,
    make_query,
    row_to_dict,
)
from tables.candidate.candidate import (
    Candidate as TCandidate,
    enums_to_module,
    candidate_syntax,
)


class Candidate(Methods):
    def __init__(self, app):
        post_methods = [
            self.candidate_authentication_token,
            self.candidate_register,
            self.candidate_get_profile,
            self.candidate_update_profile,
        ]

        get_methods = [self.candidate]

        Methods.__init__(
            self, app=app, post_methods=post_methods, get_methods=get_methods
        )
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

    def candidate_update_profile(self):
        input_json = request.get_json(force=True)
        candidate_id = input_json.pop("id")
        query, session = make_query(
            TCandidate, TCandidate.id == candidate_id, end_session=False
        )
        self.replace(session, query.first(), input_json)
        result = jsonify({})
        result.status_code = 200
        return result

    def candidate_get_profile(self):
        input_json = request.get_json(force=True)
        candidate = row_to_dict(
            make_query(TCandidate, TCandidate.id == input_json["id"]).one()
        )
        result = jsonify(
            {"instance": candidate, "syntax": candidate_syntax[candidate["language"]]}
        )
        result.status_code = 200
        return result

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

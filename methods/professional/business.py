from flask import jsonify, request

from methods.base import Methods
from methods.common import make_query, replace, row_to_dict
from tables.professional.business import Business as TBusiness


class Business(Methods):
    def __init__(self):
        post_rules = [self.get_business, self.update_business_fields]
        Methods.__init__(self, post_methods=post_rules)

    def get_business(self):
        input_json = request.get_json(force=True)
        professional_id = input_json["professional_id"]
        result = row_to_dict(
            make_query(TBusiness, TBusiness.professional_id == professional_id).first()
        )
        result = jsonify(result)
        result.status_code = 200
        return result

    def update_business_fields(self):
        input_json = request.get_json(force=True)
        professional_id = input_json.pop("professional_id")
        query, session = make_query(
            TBusiness, TBusiness.professional_id == professional_id, end_session=False
        )
        replace(session, query.first(), input_json)
        result = jsonify({})
        result.status_code = 200
        return result

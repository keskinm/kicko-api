import base64
import io
import json

import qrcode

from methods.base import Methods
from flask import request, jsonify

import syntax
from methods.common import (
    add_row,
    delete_row,
    make_query,
    row_to_dict,
    unique,
)
from tables.candidate.candidate import Candidate
from tables.professional.business import Business
from tables.professional.job_offers import JobOffers as TJobOffers


class JobOffers(Methods):
    def __init__(self, app):
        post_rules = [
            self.professional_get_job_offers,
            self.candidate_get_job_offer,
            self.candidate_get_job_offers,
            self.add_job_offer,
            self.applied_job_offer,
            self.delete_job_offer,
        ]
        Methods.__init__(self, app=app, post_methods=post_rules)

    def professional_get_job_offers(self):
        input_json = request.get_json(force=True)
        legit_business = unique(
            Business, "id", Business.professional_id == input_json["professional_id"]
        )

        result = make_query(TJobOffers, TJobOffers.business_id.in_(legit_business))
        result = [row_to_dict(o) for o in result]
        result = jsonify(list(result))
        result.status_code = 200
        return result

    def candidate_get_job_offer(self):
        input_json = request.get_json(force=True)
        result = make_query(TJobOffers, TJobOffers.id == input_json["id"]).one()
        result = jsonify(row_to_dict(result))
        result.status_code = 200
        return result

    def candidate_get_job_offers(self):
        input_json = request.get_json(force=True)
        filters = []
        if "city" in input_json and input_json["city"] != syntax.all_cities:
            legit_business = make_query(Business, Business.city == input_json["city"])
            legit_business = [row_to_dict(o) for o in legit_business]
            legit_business = list(map(lambda d: d["id"], legit_business))
            legit_business = list(set(legit_business))
            filters.append(TJobOffers.business_id.in_(legit_business))

        if len(filters) < 1:
            filters = None
        elif len(filters) < 2:
            filters = filters[0]

        result = make_query(TJobOffers, filters)
        result = [row_to_dict(o) for o in result]
        result = jsonify(list(result))
        result.status_code = 200
        return result

    def add_job_offer(self):
        input_json = request.get_json(force=True)
        new_job_offer, session = add_row(TJobOffers, input_json, end_session=False)
        new_job_offer_id = new_job_offer.id
        session.close()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(new_job_offer_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        r_dict = {}
        r_dict["img"] = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
        return json.dumps(r_dict)

    def applied_job_offer(self):
        input_json = request.get_json(force=True)
        job_offer_query, session = make_query(
            TJobOffers, TJobOffers.id == input_json["job_offer_id"], end_session=False
        )
        candidate_query, session = make_query(
            Candidate,
            Candidate.id == input_json["candidate_id"],
            end_session=False,
            session=session,
        )
        job_offer = job_offer_query.one()
        candidate = candidate_query.one()
        result = candidate in job_offer.candidate
        session.close()
        result = jsonify(result)
        result.status_code = 200
        return result

    def delete_job_offer(self):
        input_json = request.get_json(force=True)

        legit_business = unique(
            Business, "id", Business.professional_id == input_json["professional_id"]
        )

        job_offer_id = input_json["id"]
        delete_row(
            TJobOffers,
            [TJobOffers.business_id.in_(legit_business), TJobOffers.id == job_offer_id],
        )
        resp = jsonify({})
        resp.status_code = 200
        return resp

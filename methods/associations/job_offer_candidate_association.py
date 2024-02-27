from flask import jsonify, request

from app import app
from methods.associations.base import Association
from methods.base import Methods, instance_method_route
from methods.common import make_query, row_to_dict
from tables.candidate.candidate import Candidate
from tables.professional.job_offers import JobOffers


class JobOfferCandidate(Methods, Association):
    def __init__(self):
        post_rules = [
            self.apply_job_offer,
            self.professional_get_appliers,
        ]
        Methods.__init__(self, post_methods=post_rules)

    @instance_method_route(
        "applied_job_offer/<candidate_id>/<job_offer_id>", methods=["GET"]
    )
    def applied_job_offer(self, candidate_id, job_offer_id):
        job_offer_query, session = make_query(
            JobOffers, JobOffers.id == job_offer_id, end_session=False
        )
        candidate_query, session = make_query(
            Candidate,
            Candidate.id == candidate_id,
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

    def professional_get_appliers(self):
        input_json = request.get_json(force=True)
        professional_id = input_json.pop("professional_id")
        job_offer_query, session = make_query(
            JobOffers, JobOffers.id == professional_id, end_session=False
        )
        job_offer = job_offer_query.one()
        result = [row_to_dict(c) for c in job_offer.candidate]
        match_filters = lambda c: all([c[k] == v for k, v in input_json.items()])
        result = list(filter(match_filters, result))
        session.close()
        result = jsonify(result)
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/apply_job_offer/<candidate_id>/<job_offer_id>")
    def apply_job_offer(candidate_id, job_offer_id):
        job_offer_query, session = make_query(
            JobOffers, JobOffers.id == job_offer_id, end_session=False
        )
        candidate_query, session = make_query(
            Candidate,
            Candidate.id == candidate_id,
            end_session=False,
            session=session,
        )
        job_offer = job_offer_query.one()
        candidate = candidate_query.one()
        job_offer.candidate.append(candidate)
        session.commit()  # IS THIS NECESSARY?
        session.close()
        result = jsonify({})
        result.status_code = 200
        return result

from flask import jsonify, request

from app import app
from api.associations.base import Association
from api.base import ApiController, instance_method_route
from api.common import make_query, row_to_dict
from tables.candidate.candidate import Candidate
from tables.professional.job_offers import JobOffers


class JobOfferCandidate(ApiController, Association):
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

    @staticmethod
    @app.route("/api/professional_get_appliers/<job_offer_id>", methods=["POST"])
    def professional_get_appliers(job_offer_id):
        input_json = request.get_json(force=True)
        job_offer_query, session = make_query(
            JobOffers, JobOffers.id == job_offer_id, end_session=False
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

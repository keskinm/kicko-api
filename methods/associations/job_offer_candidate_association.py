from flask import jsonify, request

from methods.associations.base import Association
from methods.base import Methods
from methods.common import make_query, row_to_dict
from tables.candidate.candidate import Candidate
from tables.professional.job_offers import JobOffers


class JobOfferCandidate(Methods, Association):
    def __init__(self, app):
        post_rules = [
            self.applied_job_offer,
            self.apply_job_offer,
            self.professional_get_appliers,
        ]
        Methods.__init__(self, app=app, post_methods=post_rules)

    def applied_job_offer(self):
        input_json = request.get_json(force=True)
        job_offer_query, session = make_query(
            JobOffers, JobOffers.id == input_json["job_offer_id"], end_session=False
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

    def professional_get_appliers(self):
        input_json = request.get_json(force=True)
        job_offer_query, session = make_query(
            JobOffers, JobOffers.id == input_json["id"], end_session=False
        )
        job_offer = job_offer_query.one()
        result = [row_to_dict(c) for c in job_offer.candidate]
        session.close()
        result = jsonify(result)
        result.status_code = 200
        return result

    def apply_job_offer(self):
        input_json = request.get_json(force=True)
        job_offer_query, session = make_query(
            JobOffers, JobOffers.id == input_json["job_offer_id"], end_session=False
        )
        candidate_query, session = make_query(
            Candidate,
            Candidate.id == input_json["candidate_id"],
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

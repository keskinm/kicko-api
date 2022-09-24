from flask import jsonify, request

from methods.associations.base import Association
from methods.base import Methods
from methods.common import make_query
from tables.candidate.candidate import Candidate
from tables.professional.job_offers import JobOffers


class JobOfferCandidate(Methods, Association):
    def __init__(self, app):
        url_rules = {
            "/api/apply_job_offer": {
                "view_func": self.apply_job_offer,
                "methods": ["POST"],
            }
        }
        Methods.__init__(self, app=app, url_rules=url_rules)

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

import os
from app import app
from methods.associations.job_offer_candidate_association import JobOfferCandidate
from methods.candidate.candidate import Candidate
from methods.professional.business import Business
from methods.professional.job_offers import JobOffers
from methods.professional.professional import Professional
from methods.base import to_register_methods

from flask_cors import CORS


app.secret_key = os.urandom(12)


JobOfferCandidate(), JobOffers(), Business(), Professional()

candidate = Candidate()
app.route("/api/candidate_update_profile/<candidate_id>", methods=["POST"])(
    candidate.candidate_update_profile
)


CORS(app)


def is_method_in_url_map(method_name):
    for rule in app.url_map.iter_rules():
        if rule.endpoint == method_name:
            return True
    return False


def check_to_register_routes():
    for method in to_register_methods:
        if not is_method_in_url_map(method.__name__):
            raise RuntimeError(f"La méthode {method.__name__} n'est pas enregistrée.")


check_to_register_routes()


@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import os

from flask_cors import CORS

from app import app

# @todo -------------- FACTORY A UTILISER
from api.associations.job_offer_candidate_association import JobOfferCandidate
from api.base import register_instance_methods
from api.candidate.candidate import Candidate
from api.professional.business import Business
from api.professional.job_offers import JobOffers
from api.professional.professional import Professional

app.secret_key = os.urandom(12)

for variable in ["GOOGLE_CREDENTIALS"]:
    if not os.environ.get(variable):
        raise RuntimeError(f"Environment variable {variable} is unset.")

for _class in [Candidate, Professional, Business, JobOffers, JobOfferCandidate]:
    register_instance_methods(app, _class())

CORS(app)


@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

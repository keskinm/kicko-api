import os
from app import app
from methods.associations.job_offer_candidate_association import JobOfferCandidate
from methods.candidate.candidate import Candidate
from methods.professional.business import Business
from methods.professional.job_offers import JobOffers
from methods.professional.professional import Professional
from flask_cors import CORS


app.secret_key = os.urandom(12)


JobOfferCandidate(), JobOffers(), Business(), Professional()

candidate = Candidate()
app.route("/api/candidate_update_profile/<candidate_id>", methods=["POST"])(
    candidate.candidate_update_profile
)


CORS(app)


@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

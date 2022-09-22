import os

from flask import Flask
from flask_cors import CORS

from methods.associations.job_offer_candidate_association import JobOfferCandidate
from methods.candidate.candidate import Candidate
from methods.professional.business import Business
from methods.professional.job_offers import JobOffers
from methods.professional.professional import Professional

app = Flask(__name__)
app.secret_key = os.urandom(12)

CORS(app)


JobOfferCandidate(app), JobOffers(app), Business(app), Professional(app), Candidate(app)


@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

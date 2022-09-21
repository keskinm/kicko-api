import os

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from sqlalchemy import and_

import syntax
from models import encode_auth_token, decode_auth_token
from queries.common import (
    add_row,
    delete_row,
    make_query,
    row_to_dict,
    replace,
    unique,
)
from tables.candidate.candidate import Candidate
from tables.professional.business import Business

from tables.professional.job_offers import JobOffers
from tables.professional.professional import Professional

app = Flask(__name__)
app.secret_key = os.urandom(12)

CORS(app)


@app.route("/api/professional", methods=["GET"])
def get_professional():
    auth_header = request.headers.get("Authorization")
    return get_user(table=Professional, auth_header=auth_header)


@app.route("/api/candidate", methods=["GET"])
def get_candidate():
    auth_header = request.headers.get("Authorization")
    return get_user(table=Candidate, auth_header=auth_header)


def get_user(table, auth_header):
    if auth_header:
        print("AUTH TOKEN NON VIDE")
        auth_token = auth_header.split(" ")[1]

        succeed, resp = decode_auth_token(auth_token, app.config.get("SECRET_KEY"))
        if succeed:
            user = make_query(table, filters=table.email == resp).first()
            response_object = {
                "status": "success",
                "data": {
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "id": str(user.id),
                },
            }
            return make_response(jsonify(response_object)), 200
        response_object = {"status": "fail", "message": resp}
        return make_response(jsonify(response_object)), 401

    else:
        # @todo Why a double call everytime with the first one here?
        # Find why and then put fail and 401 response status
        response_object = {
            "status": "success",
            "message": "Provide a valid auth token.",
        }
        return make_response(jsonify(response_object)), 200


@app.route("/api/get_business", methods=["POST"])
def get_business():
    input_json = request.get_json(force=True)
    professional_id = input_json["professional_id"]
    result = row_to_dict(
        make_query(Business, Business.professional_id == professional_id).first()
    )
    result = jsonify(result)
    result.status_code = 200
    return result


@app.route("/api/update_business_fields", methods=["POST"])
def update_business_fields():
    input_json = request.get_json(force=True)
    professional_id = input_json.pop("professional_id")
    query, session = make_query(
        Business, Business.professional_id == professional_id, end_session=False
    )
    replace(session, query.first(), input_json)
    result = jsonify({})
    result.status_code = 200
    return result


@app.route("/api/professional_get_job_offers", methods=["POST"])
def professional_get_job_offers():
    input_json = request.get_json(force=True)
    legit_business = unique(
        Business, "id", Business.professional_id == input_json["professional_id"]
    )

    result = make_query(JobOffers, JobOffers.business_id.in_(legit_business))
    result = [row_to_dict(o) for o in result]
    result = jsonify(list(result))
    result.status_code = 200
    return result


@app.route("/api/candidate_get_job_offers", methods=["POST"])
def candidate_get_job_offers():
    input_json = request.get_json(force=True)
    filters = []
    if "city" in input_json and input_json["city"] != syntax.all_cities:
        legit_business = make_query(Business, Business.city == input_json["city"])
        legit_business = [row_to_dict(o) for o in legit_business]
        legit_business = list(map(lambda d: d["id"], legit_business))
        legit_business = list(set(legit_business))
        filters.append(JobOffers.business_id.in_(legit_business))

    if len(filters) < 1:
        filters = None
    elif len(filters) < 2:
        filters = filters[0]

    result = make_query(JobOffers, filters)
    result = [row_to_dict(o) for o in result]
    result = jsonify(list(result))
    result.status_code = 200
    return result


@app.route("/api/add_job_offer", methods=["POST"])
def add_job_offer():
    input_json = request.get_json(force=True)
    add_row(JobOffers, input_json)
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/apply_job_offer", methods=["POST"])
def apply_job_offer():
    # @todo to be redo with relationships
    input_json = request.get_json(force=True)
    job_offer, session = make_query(
        JobOffers, JobOffers.id == input_json["job_offer_id"], end_session=False
    )
    candidate, session = make_query(
        Candidate,
        Candidate.id == input_json["candidate_id"],
        end_session=False,
        session=session,
    )
    job_offer.one().candidate.append(candidate.one())
    session.commit()  # IS THIS NECESSARY?
    session.close()
    result = jsonify({})
    result.status_code = 200
    return result


@app.route("/api/delete_job_offer", methods=["POST"])
def delete_job_offer():
    input_json = request.get_json(force=True)

    legit_business = unique(
        Business, "id", Business.professional_id == input_json["professional_id"]
    )

    job_offer_id = input_json["id"]
    delete_row(
        JobOffers,
        [JobOffers.business_id.in_(legit_business), JobOffers.id == job_offer_id],
    )
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/professional_register", methods=["POST"])
def professional_register():
    input_json = request.get_json(force=True)
    add_row(Professional, input_json)
    professional_id = row_to_dict(
        make_query(Professional, Professional.email == input_json["email"]).first()
    )
    add_row(Business, {"professional_id": professional_id["id"]})
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/candidate_register", methods=["POST"])
def candidate_register():
    input_json = request.get_json(force=True)
    add_row(Candidate, input_json)
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/professional-authentication-token", methods=["POST"])
def professional_get_token():
    input_json = request.get_json(force=True)
    return get_token(table=Professional, input_json=input_json)


@app.route("/api/candidate-authentication-token", methods=["POST"])
def candidate_get_token():
    input_json = request.get_json(force=True)
    return get_token(table=Candidate, input_json=input_json)


def get_token(table, input_json):
    username = input_json["username"]
    password = input_json["password"]
    query_result = make_query(
        Professional,
        filters=and_(table.username == username, table.password == password),
    ).first()
    if query_result:
        token = encode_auth_token(username, app.config.get("SECRET_KEY"))
        result = jsonify({"token": token})
        result.status_code = 200
    else:
        result = jsonify({})
        # result.status_code = 401
    return result


@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

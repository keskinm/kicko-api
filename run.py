import os

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

from add.add import Add
from models import encode_auth_token, decode_auth_token

from queries.queries import Queries
from tables.professional.job_offers import JobOffers
from tables.professional.user import User

app = Flask(__name__)
app.secret_key = os.urandom(12)

CORS(app)

q = Queries()
add = Add()


@app.route("/api/user", methods=["GET"])
def get_user():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        print("AUTH TOKEN NON VIDE")
        auth_token = auth_header.split(" ")[1]

        succeed, resp = decode_auth_token(auth_token, app.config.get("SECRET_KEY"))
        if succeed:
            user = q.make_query(User, filters=User.email == resp).first()
            response_object = {
                "status": "success",
                "data": {
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                },
            }
            return make_response(jsonify(response_object)), 200
        response_object = {"status": "fail", "message": resp}
        return make_response(jsonify(response_object)), 401

    else:
        # @todo Why a double call everytime with the first one here?
        # Find why and then put fail and 401 response status
        response_object = {"status": "success", "message": "Provide a valid auth token."}
        return make_response(jsonify(response_object)), 200


@app.route("/api/get_job_offers", methods=["POST"])
def get_job_offers():
    input_json = request.get_json(force=True)
    user_id = input_json["user_id"]
    result = q.make_query(JobOffers, JobOffers.user_id == user_id)
    result = [q.row_to_dict(o) for o in result]
    result = jsonify(list(result))
    result.status_code = 200
    return result


@app.route("/api/add_job_offer", methods=["POST"])
def add_job_offer():
    input_json = request.get_json(force=True)
    add.add(JobOffers, input_json)
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/user_register", methods=["POST"])
def user_register():
    input_json = request.get_json(force=True)
    add.add(User, input_json)
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/authentication-token", methods=["POST"])
def get_token():
    input_json = request.get_json(force=True)
    username = input_json["username"]
    password = input_json["password"]
    query_result = q.make_query(
        User, filters=User.username == username and User.password == password
    ).first()
    if query_result:
        token = encode_auth_token(username, app.config.get("SECRET_KEY"))
        result = jsonify({"token": token})
        result.status_code = 200
    else:
        result = jsonify({})
    return result


@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

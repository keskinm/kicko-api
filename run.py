import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from add.add import Add
from models import encode_auth_token
# from bson.json_util import dumps

from queries.queries import Queries
from tables.professional.user import User

app = Flask(__name__)
app.secret_key = os.urandom(12)

CORS(app)

q = Queries()
add = Add()


@app.route("/api/user", methods=["GET"])
def get_user():
    q.get(User)
    return jsonify({})


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
    query_result = q.get(User, filters=User.username == username and User.password == password)
    if query_result:
        token = encode_auth_token(username, app.config.get('SECRET_KEY'))
        result = jsonify({"token": token})
        result.status_code = 200
    else:
        result = jsonify({})
    return result

@app.route("/")
def home():
    return 'home'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

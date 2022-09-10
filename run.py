import os

from flask import Flask, request, jsonify
from flask_cors import CORS
# from bson.json_util import dumps

from queries.queries import Queries
from tables.professional.user import User

app = Flask(__name__)
CORS(app)

q = Queries()


@app.route("/api/user", methods=["GET"])
def get_user():
    q.get(User)
    return jsonify({})


app.secret_key = os.urandom(12)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

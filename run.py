import os

from flask_cors import CORS

from app import app

from api.base import register_instance_methods
from api.controllers_factory import controllers

app.secret_key = os.urandom(12)

for variable in ["GOOGLE_CREDENTIALS"]:
    if not os.environ.get(variable):
        raise RuntimeError(f"Environment variable {variable} is unset.")

for controller in controllers:
    register_instance_methods(app, controller())

CORS(app)

@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import os

from flask_cors import CORS
from settings import set_local_settings

from app import app

set_local_settings(app)
app.secret_key = os.urandom(12)
CORS(app)

@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

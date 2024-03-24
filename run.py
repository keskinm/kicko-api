import os

from flask_cors import CORS
from settings import LocalSettings, ProdSettings

from app import app

settings_group = os.environ.get("SETTINGS_GROUP", None)
if settings_group == "LOCAL":
    LocalSettings(app)
elif settings_group == "PROD":
    ProdSettings(app)
else:
    raise ValueError("SETTINGS_GROUP should be in ['LOCAL', 'PROD']")

app.secret_key = os.urandom(12)
CORS(app)


@app.route("/")
def home():
    return "home"

if settings_group == "LOCAL" and __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

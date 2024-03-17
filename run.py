import os

from flask_cors import CORS
from settings import LocalSettings
from flask import request
import json

from app import app

LocalSettings(app)
app.secret_key = os.urandom(12)
CORS(app)


@app.after_request
def log_response(response):
    os.makedirs("metrics", exist_ok=True)
    if response.data and 'application/json' in response.content_type:
        route_name = request.endpoint
        try:
            json_data = json.loads(response.data.decode('utf-8'))
            with open(f"metrics/{route_name}.json", "w") as outfile:
                json.dump(json_data, outfile)
        except json.JSONDecodeError as e:
            print(f"Erreur lors du décodage JSON pour la route {route_name}: {e}")
    else:
        print(f"Réponse non-JSON ou vide pour la route {request.endpoint}")
    return response



@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import os
from flask import request
import json

from firebase_admin import credentials, exceptions, get_app, initialize_app
from api.base import register_instance_methods
from api.controllers_factory import controllers



class CommonSettings:
    def __init__(self, app):
        self.app = app
        self.set_settings()
    def set_settings(self):
        for controller in controllers:
            register_instance_methods(self.app, controller())


class LocalSettings(CommonSettings):
    def __init__(self, app):
        super().__init__(app)

    def set_settings(self):
        super().set_settings()
        for variable in ["GOOGLE_CREDENTIALS"]:
            if not os.environ.get(variable):
                raise RuntimeError(f"Environment variable {variable} is unset.")
        cred = credentials.Certificate(os.environ.get("GOOGLE_CREDENTIALS"))
        initialize_app(cred, {"storageBucket": "kicko-b75db.appspot.com"})
        self.register_after_request_hooks()

    def register_after_request_hooks(self):
        @self.app.after_request
        def log_response(response):
            os.makedirs("metrics", exist_ok=True)
            if response.data and 'application/json' in response.content_type:
                route_name = request.endpoint
                try:
                    json_data = json.loads(response.data.decode('utf-8'))
                    file_path = f"metrics/{route_name}.json"

                    if os.path.exists(file_path):
                        with open(file_path, "r") as infile:
                            try:
                                existing_data = json.load(infile)
                            except json.JSONDecodeError:
                                existing_data = []
                    else:
                        existing_data = []

                    existing_data.append(json_data)
                    with open(file_path, "w") as outfile:
                        json.dump(existing_data, outfile)
                except json.JSONDecodeError as e:
                    print(f"Erreur lors du décodage JSON pour la route {route_name}: {e}")
            else:
                print(f"Réponse non-JSON ou vide pour la route {request.endpoint}")
            return response


class TestSettings(CommonSettings):
    def __init__(self, app):
        super().__init__(app)


class ProdSettings(CommonSettings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError

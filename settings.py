import os

from firebase_admin import credentials, exceptions, get_app, initialize_app
from api.base import register_instance_methods
from api.controllers_factory import controllers

def set_local_settings(app):
    for variable in ["GOOGLE_CREDENTIALS"]:
        if not os.environ.get(variable):
            raise RuntimeError(f"Environment variable {variable} is unset.")

    for controller in controllers:
        register_instance_methods(app, controller())

    cred = credentials.Certificate(os.environ.get("GOOGLE_CREDENTIALS"))
    initialize_app(cred, {"storageBucket": "kicko-b75db.appspot.com"})


def set_test_settings(app):
    for controller in controllers:
        register_instance_methods(app, controller())

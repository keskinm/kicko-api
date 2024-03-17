import os

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


class TestSettings(CommonSettings):
    def __init__(self, app):
        super().__init__(app)



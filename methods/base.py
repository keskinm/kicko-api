from tables.candidate.candidate import Candidate
from tables.professional.professional import Professional
from app import app

from functools import partial, wraps


def register_instance_methods(app, instance):
    for attr_name in dir(instance):
        attr = getattr(instance, attr_name)
        if hasattr(attr, "_route") and hasattr(attr, "_methods"):
            endpoint = f"{instance.__class__.__name__}.{attr_name}"
            app.add_url_rule(
                f"/api/{attr._route}", endpoint, attr, methods=attr._methods
            )


def instance_method_route(route, methods=["GET"]):
    """Decorator to add instance methods."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper._route = route
        wrapper._methods = methods
        return wrapper

    return decorator


class Methods:
    def __init__(self, url_rules=None, post_methods=None, get_methods=None):
        self.url_rules = url_rules or {}

        post_methods = post_methods or []
        get_methods = get_methods or []
        self.add_post_rules(post_methods)
        self.add_get_rules(get_methods)

        self.add_url_rules()
        self.table_routes = {
            "user_group": {"candidate": Candidate, "professional": Professional}
        }

    def add_post_rules(self, post_methods, prefix="api"):
        for post_method in post_methods:
            self.url_rules.update(
                {
                    f"/{prefix}/{post_method.__name__}": {
                        "view_func": post_method,
                        "methods": ["POST"],
                    }
                }
            )

    def add_get_rules(self, get_methods, prefix="api"):
        for get_method in get_methods:
            self.url_rules.update(
                {
                    f"/{prefix}/{get_method.__name__}": {
                        "view_func": get_method,
                        "methods": ["GET"],
                    }
                }
            )

    def add_url_rules(self):
        for url, _d in self.url_rules.items():
            app.add_url_rule(url, view_func=_d["view_func"], methods=_d["methods"])

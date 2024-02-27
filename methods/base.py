from tables.candidate.candidate import Candidate
from tables.professional.professional import Professional
from app import app

to_register_methods = []


def to_register(method):
    """Decorator for methods that has to be registered manually."""
    to_register_methods.append(method)
    return method


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

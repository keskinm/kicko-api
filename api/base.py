from functools import partial, wraps

from app import app
from tables.candidate.candidate import Candidate
from tables.professional.professional import Professional


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


class ApiController:
    """Api Controller Base class."""
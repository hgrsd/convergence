from Flask import request
from functools import wraps
from .exceptions import InvalidRequestError


def validate_json(keys):
    """
    Check whether all required keys are in the json object
    Use to decorate Flask endpoint
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for key in keys:
                if key not in request.json:
                    raise InvalidRequestError(f"Missing key: {key}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

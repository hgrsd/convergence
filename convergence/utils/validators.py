import re
from flask import request
from functools import wraps

from convergence.utils.exceptions import InvalidRequestError


def contains_json_keys(keys):
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


def is_email_format(input):
    """
    Returns true if input looks like a valid email address
    Note: this is a basic check
    @TODO: Replace with confirmation email
    """
    if not isinstance(input, str) or len(input) > 254:
        return False
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]{2,}", input) is not None


def is_phone_format(input):
    """ Returns true if input looks like a valid phone number"""
    if not isinstance(input, str):
        return False
    return re.fullmatch(r"^\+*[0-9\-\s()]{7,}", input) is not None

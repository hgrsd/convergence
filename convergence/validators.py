import re
from flask import request
from functools import wraps

from .exceptions import InvalidRequestError


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
    """Returns true if input looks like a valid email address"""
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]{2,}", input) is not None


def is_phone_format(input):
    """
    Returns true if input looks like a valid phone number
    This does not actually verify the validity of the address
    """
    if len(input) > 254:  # max number of characters according to RFC3696
        return False
    return re.fullmatch(r"^\+*[0-9\-\s()]+", input) is not None

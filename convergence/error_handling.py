from flask import jsonify

from . import exceptions
from . import app


@app.errorhandler(exceptions.InvalidRequestError)
def invalid_request_error(error):
    return error_to_response(error), 400


@app.errorhandler(exceptions.LocationError)
def location_error(error):
    return error_to_response(error), 400


@app.errorhandler(exceptions.LoginError)
def login_error(error):
    return error_to_response(error), 401


@app.errorhandler(exceptions.InputError)
def username_error(error):
    return error_to_response(error), 400


@app.errorhandler(exceptions.PermissionError)
def permission_error(error):
    return error_to_response(error), 401


@app.errorhandler(exceptions.NotFoundError)
def not_found_error(error):
    return error_to_response(error), 404


@app.errorhandler(exceptions.ServerError)
def server_error(error):
    return error_to_response(error), 500


@app.errorhandler(exceptions.DatabaseError)
def database_error(error):
    return error_to_response(error), 500


def error_to_response(error):
    return jsonify({"error": {"type": type(error).__name__,
                              "message": error.message}})

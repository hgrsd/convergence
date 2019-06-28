from flask import jsonify

from . import exceptions
from . import app


@app.errorhandler(exceptions.InvalidLocation)
def location_error(error):
    return jsonify({"error": {"type": "InvalidLocation",
                              "message": error.message}}), 400


@app.errorhandler(exceptions.InvalidLogin)
def login_error(error):
    return jsonify({"error": {"type": "InvalidLogin",
                              "message": error.message}}), 401


@app.errorhandler(exceptions.AccountDetailsError)
def username_error(error):
    return jsonify({"error": {"type": "AccountDetailsError",
                              "message": error.message}}), 400


@app.errorhandler(exceptions.PermissionDenied)
def permission_error(error):
    return jsonify({"error": {"type": "PermissionDenied",
                              "message": error.message}}), 401


@app.errorhandler(exceptions.EventNotFound)
def event_not_found_error(error):
    return jsonify({"error": {"type": "EventNotFound",
                              "message": error.message}}), 404


@app.errorhandler(exceptions.UserNotFound)
def user_not_found_error(error):
    return jsonify({"error": {"type": "UserNotFound",
                              "message": error.message}}), 404


@app.errorhandler(exceptions.ServerError)
def server_error(error):
    return jsonify({"error": {"type": "ServerError",
                              "message": error.message}}), 500


@app.errorhandler(exceptions.DatabaseError)
def database_error(error):
    return jsonify({"error": {"type": "DatabaseError",
                              "message": error.message}}), 500

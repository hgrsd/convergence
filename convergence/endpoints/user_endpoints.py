import flask_jwt_extended
from flask import Blueprint, jsonify, request

from convergence.utils import validators
from convergence.utils.exceptions import InputError
from convergence.core import user

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["POST"])
@validators.contains_json_keys(["screen_name", "password", "email"])
def register_user():
    """
    Register new user
    :return: new user's full info
    """
    screen_name = request.get_json()["screen_name"]
    password = request.get_json()["password"]
    email = request.get_json()["email"].lower()
    if "phone" in request.json.keys():
        phone = request.get_json()["phone"]  # optional
    else:
        phone = None
    result = user.register_user(email, password, screen_name, phone)
    response = jsonify({"data": result})
    access_token = flask_jwt_extended.create_access_token(
        identity=result["user_id"]
    )
    flask_jwt_extended.set_access_cookies(response, access_token)
    return response, 200


@user_bp.route("/user/login", methods=["POST"])
@validators.contains_json_keys(["email", "password"])
def login():
    """
    Login user, set access cookie (JWT + CSRF token)
    :return: user id

    TODO: separate cookie-based JWT storage and response-based one.
    For security reasons, web app is not supposed to have direct access
    to the JWT and CSRF tokens.
    """
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    user_id = user.login(email, password)
    response = jsonify({"data": {"user_id": user_id}})
    access_token = flask_jwt_extended.create_access_token(identity=user_id)
    flask_jwt_extended.set_access_cookies(response, access_token)
    return response, 200


@user_bp.route("/user", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_user():
    """
    Delete current user
    :return: success status
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    user.delete_user(user_id)
    return jsonify({"success": True}), 200


@user_bp.route("/user", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_user_info():
    """
    Get info for current user
    :return: full user info
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = user.get_info(user_id)
    return jsonify({"data": result}), 200


@user_bp.route("/user/<string:email>", methods=["GET"])
@flask_jwt_extended.jwt_required
def find_user(email):
    """
    Find user info by email
    :return: basic user info
    """
    result = user.find_user(email)
    return jsonify({"data": result}), 200


@user_bp.route("/user/location", methods=["PUT"])
@flask_jwt_extended.jwt_required
@validators.contains_json_keys(["latitude", "longitude"])
def update_location():
    """
    Update current user"s location
    :param lat: current latitude, float
    :param long: current longitude, float
    :return: updated location info
    """
    try:
        lat = float(request.get_json()["latitude"])
        long = float(request.get_json()["longitude"])
    except ValueError:
        raise InputError("Latitude and longitude must be numbers.")
    user_id = flask_jwt_extended.get_jwt_identity()
    result = user.update_location(user_id, lat, long)
    return jsonify({"data": result}), 200

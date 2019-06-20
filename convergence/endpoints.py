from flask import Blueprint, g, jsonify, request
import flask_jwt_extended
from . import groups, location, user, suggestions
from . import app

user_bp = Blueprint("user", __name__)
groups_bp = Blueprint("groups", __name__)
location_bp = Blueprint("locations", __name__)
suggestions_bp = Blueprint("suggestions", __name__)


# -- web interface
@app.route("/", methods=['GET'])
def root():
    return app.send_static_file('index.html')

# -- user endpoints:
@user_bp.route("/user", methods=["POST"])
def register_user():
    """
    Register new user
    :return: HTTP response
    """
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    response = user.register_user(username, password)
    return jsonify(response["body"]), response["status_code"]


@user_bp.route("/user/login", methods=["POST"])
def login():
    """
    Login user
    :return: HTTP response
    """
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    response = user.login(username, password)
    return jsonify(response["body"]), response["status_code"]


@user_bp.route("/user", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_user():
    """
    Delete current user
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = user.delete_user(user_id)
    return jsonify(response["body"]), response["status_code"]


@user_bp.route("/user", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_user_info():
    """
    Get info for current user 
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = user.get_info(user_id)
    return jsonify(response["body"]), response["status_code"]


@user_bp.route("/user/<string:username>", methods=["GET"])
@flask_jwt_extended.jwt_required
def find_user(username):
    """
    Find user info by username
    :return: HTTP response
    """
    response = user.find_user(username)
    return jsonify(response["body"]), response["status_code"]

@user_bp.route("/user/availability/<int:available>", methods=["PUT"])
@flask_jwt_extended.jwt_required
def set_availability(available):
    """
    Update current user"s availability
    :param available: 0 = False, 1 = True
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = user.set_availability(user_id, bool(available))
    return jsonify(response["body"]), response["status_code"]


# -- location endpoints:
@location_bp.route("/loc/<float:lat>:<float:long>", methods=["PUT"])
@flask_jwt_extended.jwt_required
def update_location(lat, long):
    """
    Update current user"s location
    :param lat: current latitude, float
    :param long: current longitude, float
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = location.update_location(user_id, lat, long)
    return jsonify(response["body"]), response["status_code"]


# -- group endpoints:
@groups_bp.route("/groups/<string:name>", methods=["POST"])
@flask_jwt_extended.jwt_required
def create_group(name):
    """
    Create new group, owned by current user
    :param name: group name
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = groups.create_group(user_id, name)
    return jsonify(response["body"]), response["status_code"]


@groups_bp.route("/groups/<int:group_id>", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_group(group_id):
    """
    Delete group (requesting user must be group owner)
    :param group_id: group to be deleted
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = groups.delete_group(user_id, group_id)
    return jsonify(response["body"]), response["status_code"]


@groups_bp.route("/groups/owned", methods=["GET"])
@flask_jwt_extended.jwt_required
def owned_groups():
    """
    Get groups owned by user
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = groups.get_owned_groups(user_id)
    return jsonify(response["body"]), response["status_code"]


@groups_bp.route("/groups/user_group/<int:group_id>:<int:user_id>", methods=["POST"])
@flask_jwt_extended.jwt_required
def add_user_to_group(group_id, user_id):
    """
    Add user to group (requesting user must be group owner)
    :param group_id: group to add user to
    :param user_id: user to add to group
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    response = groups.add_user_to_group(request_id, user_id, group_id)
    return jsonify(response["body"]), response["status_code"]


@groups_bp.route("/groups/user_group/<int:group_id>:<int:user_id>", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def remove_user_from_group(group_id, user_id):
    """
    Remove user from group (requesting user must be group owner)
    :param group_id: group to remove user from
    :param user_id: user to remove from group
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    response = groups.remove_user_from_group(request_id, user_id, group_id)
    return jsonify(response["body"]), response["status_code"]


@groups_bp.route("/groups/<int:group_id>:<int:available>", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_members(group_id, available):
    """
    Get list of group members (requesting user must be group member)
    :param group_id: group to request members from
    :param available: limit results to available members, 0 = False, 1 = True
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    if available == 1:
        response = groups.get_available_members(user_id, group_id)
    else:
        response = groups.get_members(user_id, group_id)
    return jsonify(response["body"]), response["status_code"]


@groups_bp.route("/groups", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_groups():
    """
    Get groups of which requesting user is a member.
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    response = groups.get_groups(user_id)
    return jsonify(response["body"]), response["status_code"]


# -- suggestions endpoints:
@suggestions_bp.route("/suggestions/distance/<int:group_id>:<string:place_type>", methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_distance(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average distance as-the-crow-flies
    for group members.
    :param group_id: group to request suggestions for
    :param place_type: type of place
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    response = suggestions.get_suggestions(request_id, group_id, place_type, "distance")
    return jsonify(response["body"]), response["status_code"]


@suggestions_bp.route("/suggestions/transit/<int:group_id>:<string:place_type>", methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_transit(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, using public transport.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    response = suggestions.get_suggestions(request_id, group_id, place_type, "transit")
    return jsonify(response["body"]), response["status_code"]


@suggestions_bp.route("/suggestions/drive/<int:group_id>:<string:place_type>", methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_driving(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, driving.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    response = suggestions.get_suggestions(request_id, group_id, place_type, "driving")
    return jsonify(response["body"]), response["status_code"]


@suggestions_bp.route("/suggestions/walk/<int:group_id>:<string:place_type>", methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_walking(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, walking.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    response = suggestions.get_suggestions(request_id, group_id, place_type, "walking")
    return jsonify(response["body"]), response["status_code"]


@suggestions_bp.route("/suggestions/cycle/<int:group_id>:<string:place_type>", methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_bicycling(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, cycling.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    response = suggestions.get_suggestions(request_id, group_id, place_type, "bicycling")
    return jsonify(response["body"]), response["status_code"]


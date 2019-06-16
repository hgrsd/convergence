from flask import Blueprint, g, jsonify
from . import http_auth
from . import groups, location, user, suggestions

user_bp = Blueprint("user", __name__)
groups_bp = Blueprint("groups", __name__)
location_bp = Blueprint("locations", __name__)
suggestions_bp = Blueprint("suggestions", __name__)


# -- user endpoints:
@user_bp.route("/user/<string:username>:<string:password>", methods=['POST'])
def register_user(username, password):
    """
    Register new user
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = user.register_user(username, password)
    return jsonify(response[0]), response[1]


@user_bp.route("/user", methods=['DELETE'])
@http_auth.login_required
def delete_user():
    """
    Delete current user
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = user.delete_user(g.user_id)
    return jsonify(response[0]), response[1]


@user_bp.route("/user/availability/<int:available>", methods=['PUT'])
@http_auth.login_required
def set_availability(available):
    """
    Update current user's availability
    :param available: 0 = False, 1 = True
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = user.set_availability(g.user_id, bool(available))
    return jsonify(response[0]), response[1]


# -- location endpoints:
@location_bp.route("/loc/<float:lat>:<float:long>", methods=['PUT'])
@http_auth.login_required
def update_location(lat, long):
    """
    Update current user's location
    :param lat: current latitude, float
    :param long: current longitude, float
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = location.update_location(g.user_id, lat, long)
    return jsonify(response[0]), response[1]


# -- group endpoints:
@groups_bp.route('/groups/<string:name>', methods=['POST'])
@http_auth.login_required
def create_group(name):
    """
    Create new group, owned by current user
    :param name: group name
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = groups.create_group(g.user_id, name)
    return jsonify(response[0]), response[1]


@groups_bp.route('/groups/<int:group_id>', methods=['DELETE'])
@http_auth.login_required
def delete_group(group_id):
    """
    Delete group (requesting user must be group owner)
    :param group_id: group to be deleted
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = groups.delete_group(g.user_id, group_id)
    return jsonify(response[0]), response[1]


@groups_bp.route('/groups/user_group/<int:group_id>:<int:user_id>', methods=['POST'])
@http_auth.login_required
def add_user_to_group(group_id, user_id):
    """
    Add user to group (requesting user must be group owner)
    :param group_id: group to add user to
    :param user_id: user to add to group
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = groups.add_user_to_group(g.user_id, user_id, group_id)
    return jsonify(response[0]), response[1]


@groups_bp.route('/groups/user_group/<int:group_id>:<int:user_id>', methods=['DELETE'])
@http_auth.login_required
def remove_user_from_group(group_id, user_id):
    """
    Remove user from group (requesting user must be group owner)
    :param group_id: group to remove user from
    :param user_id: user to remove from group
    :return: HTTP response(JSON-object (status message), status code)
    """
    response = groups.remove_user_from_group(g.user_id, user_id, group_id)
    return jsonify(response[0]), response[1]


@groups_bp.route('/groups/<int:group_id>:<int:available>', methods=['GET'])
@http_auth.login_required
def get_members(group_id, available):
    """
    Get list of group members (requesting user must be group member)
    :param group_id: group to request members from
    :param available: limit results to available members, 0 = False, 1 = True
    :return: HTTP response(JSON-object (data and status message), status code)
    """
    if available == 1:
        response = groups.get_available_members(g.user_id, group_id)
    else:
        response = groups.get_members(g.user_id, group_id)
    return jsonify(response[0]), response[1]


@groups_bp.route('/groups', methods=['GET'])
@http_auth.login_required
def get_groups():
    """
    Get groups of which requesting user is a member.
    :return: HTTP response(JSON-object (data and status message), status code)
    """
    response = groups.get_groups(g.user_id)
    return jsonify(response[0]), response[1]


# -- suggestions endpoints:
@suggestions_bp.route('/suggestions/distance/<int:group_id>:<string:place_type>', methods=['GET'])
@http_auth.login_required
def suggestions_distance(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average distance as-the-crow-flies
    for group members.
    :param group_id: group to request suggestions for
    :param place_type: type of place
    :return: HTTP response(JSON-object (data and status message), status code)
    """
    request_id = g.user_id
    response = suggestions.get_suggestions(request_id, group_id, place_type, "distance")
    return jsonify(response[0]), response[1]


@suggestions_bp.route('/suggestions/transit/<int:group_id>:<string:place_type>', methods=['GET'])
@http_auth.login_required
def suggestions_transit(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, using public transport.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response(JSON-object (data and status message), status code)
    """
    request_id = g.user_id
    response = suggestions.get_suggestions(request_id, group_id, place_type, "transit")
    return jsonify(response[0]), response[1]


@suggestions_bp.route('/suggestions/drive/<int:group_id>:<string:place_type>', methods=['GET'])
@http_auth.login_required
def suggestions_driving(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, driving.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response(JSON-object (data and status message), status code)
    """
    request_id = g.user_id
    response = suggestions.get_suggestions(request_id, group_id, place_type, "driving")
    return jsonify(response[0]), response[1]


@suggestions_bp.route('/suggestions/walk/<int:group_id>:<string:place_type>', methods=['GET'])
@http_auth.login_required
def suggestions_walking(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, walking.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response(JSON-object (data and status message), status code)
    """
    request_id = g.user_id
    response = suggestions.get_suggestions(request_id, group_id, place_type, "walking")
    return jsonify(response[0]), response[1]


@suggestions_bp.route('/suggestions/cycle/<int:group_id>:<string:place_type>', methods=['GET'])
@http_auth.login_required
def suggestions_bicycling(group_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for group
    members, cycling.
    :param group_id: group to request suggestions for
    :param place_type: type of places
    :return: HTTP response(JSON-object (data and status message), status code)
    """
    request_id = g.user_id
    response = suggestions.get_suggestions(request_id, group_id, place_type, "bicycling")
    return jsonify(response[0]), response[1]


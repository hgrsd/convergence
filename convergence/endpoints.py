from flask import Blueprint, request, g, jsonify
from . import http_auth
from . import groups, location, auth, core

auth_bp = Blueprint("auth", __name__)
groups_bp = Blueprint("groups", __name__)
location_bp = Blueprint("locations", __name__)
core_bp = Blueprint("core", __name__)

# -- auth endpoints:
@auth_bp.route('/auth/register', methods=['POST'])
def register_user():
    username = request.json.get('username')
    password = request.json.get('password')
    return auth.register_user(username, password)


# -- location endpoints:
@location_bp.route("/loc/update_location", methods=['POST'])
@http_auth.login_required
def update_location():
    lat = request.json.get("lat")
    long = request.json.get("long")
    return location.update_location(g.user_id, lat, long)


# -- group endpoints:
@groups_bp.route('/groups/create_group', methods=['POST'])
@http_auth.login_required
def create_group():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": {"message": "please provide group name"}}), 400
    return groups.create_group(g.user_id, name)


@groups_bp.route('/groups/add_user_to_group', methods=['POST'])
@http_auth.login_required
def add_user_to_group():
    group_id = request.json.get('group_id')
    user_id = request.json.get('user_id')
    return groups.add_user_to_group(g.user_id, user_id, group_id)


@groups_bp.route('/groups/remove_user_from_group', methods=['POST'])
@http_auth.login_required
def remove_user_from_group():
    group_id = request.json.get('group_id')
    user_id = request.json.get('user_id')
    return groups.remove_user_from_group(g.user_id, user_id, group_id)


@groups_bp.route('/groups/get_members', methods=['GET'])
@http_auth.login_required
def get_members():
    group_id = request.json.get('group_id')
    return groups.get_members(g.user_id, group_id)


@groups_bp.route('/groups/get_user_groups', methods=['GET'])
@http_auth.login_required
def get_groups():
    return groups.get_groups(g.user_id)


# -- core endpoints:
@core_bp.route('/core/get_suggestions', methods=['GET'])
@http_auth.login_required
def get_suggestions():
    request_id = g.user_id
    group_id = request.json.get('group_id')
    place_type = request.json.get('type')
    return core.get_suggestions(request_id, group_id, place_type)
import flask_jwt_extended
from flask import Blueprint, jsonify, request

from . import events, user, suggestions
from . import app

user_bp = Blueprint("user", __name__)
events_bp = Blueprint("events", __name__)
location_bp = Blueprint("locations", __name__)
suggestions_bp = Blueprint("suggestions", __name__)


# -- web interface
@app.route("/",
           methods=['GET'])
def root():
    return app.send_static_file('index.html')

# -- user endpoints:
@user_bp.route("/user",
               methods=["POST"])
def register_user():
    """
    Register new user
    :return: HTTP response
    """
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    email = request.get_json()["email"]
    phone_number = request.get_json()["phone_number"]
    result = user.register_user(username, password, email, phone_number)
    return jsonify({"data": result}), 200


@user_bp.route("/user/login",
               methods=["POST"])
def login():
    """
    Login user
    :return: HTTP response

    TODO: separate cookie-based JWT storage and response-based one.
    For security reasons, web app is not supposed to have direct access
    to the JWT and CSRF tokens.
    """
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    user_id = user.login(username, password)
    access_token = flask_jwt_extended.create_access_token(identity=user_id)
    response = jsonify({"success": True})
    flask_jwt_extended.set_access_cookies(response, access_token)
    return response, 200


@user_bp.route("/user",
               methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_user():
    """
    Delete current user
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    user.delete_user(user_id)
    return jsonify({"success": True}), 200


@user_bp.route("/user",
               methods=["GET"])
@flask_jwt_extended.jwt_required
def get_user_info():
    """
    Get info for current user
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = user.get_info(user_id)
    return jsonify({"data": result}), 200


@user_bp.route("/user/<string:username>",
               methods=["GET"])
@flask_jwt_extended.jwt_required
def find_user(username):
    """
    Find user info by username
    :return: HTTP response
    """
    result = user.find_user(username)
    return jsonify({"data": result}), 200


@user_bp.route("/user/location/<float:lat>:<float:long>",
               methods=["PUT"])
@flask_jwt_extended.jwt_required
def update_location(lat, long):
    """
    Update current user"s location
    :param lat: current latitude, float
    :param long: current longitude, float
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = user.update_location(user_id, lat, long)
    return jsonify({"data": result}), 200


# -- event endpoints:
@events_bp.route("/events/<string:name>",
                 methods=["POST"])
@flask_jwt_extended.jwt_required
def create_event(name):
    """
    Create new event, owned by current user
    :param name: event name
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = events.create_event(user_id, name)
    return jsonify({"data": result}), 200


@events_bp.route("/events/<int:event_id>",
                 methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_event(event_id):
    """
    Delete event (requesting user must be event owner)
    :param event_id: event to be deleted
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    events.delete_event(user_id, event_id)
    return jsonify({"success": True}), 200


@events_bp.route("/events/owned",
                 methods=["GET"])
@flask_jwt_extended.jwt_required
def owned_events():
    """
    Get events owned by user
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = events.get_owned_events(user_id)
    return jsonify({"data": result}), 200


@events_bp.route("/events/user_event/<int:event_id>:<int:user_id>",
                 methods=["POST"])
@flask_jwt_extended.jwt_required
def add_user_to_event(event_id, user_id):
    """
    Add user to event (requesting user must be event owner)
    :param event_id: event to add user to
    :param user_id: user to add to event
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    events.add_user_to_event(request_id, user_id, event_id)
    return jsonify({"success": True}), 200


@events_bp.route("/events/user_event/<int:event_id>:<int:user_id>",
                 methods=["DELETE"])
@flask_jwt_extended.jwt_required
def remove_user_from_event(event_id, user_id):
    """
    Remove user from event (requesting user must be event owner)
    :param event_id: event to remove user from
    :param user_id: user to remove from event
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    events.remove_user_from_event(request_id, user_id, event_id)
    return jsonify({"success": True}), 200


@events_bp.route("/events/<int:event_id>",
                 methods=["GET"])
@flask_jwt_extended.jwt_required
def get_members(event_id):
    """
    Get list of event members (requesting user must be event member)
    :param event_id: event to request members from
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = events.get_members(user_id, event_id)
    return jsonify({"data": result}), 200

@events_bp.route("/events",
                 methods=["GET"])
@flask_jwt_extended.jwt_required
def get_events():
    """
    Get events of which requesting user is a member.
    :return: HTTP response
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = events.get_events(user_id)
    return jsonify({"data": result}), 200

# -- suggestions endpoints:
@suggestions_bp.route("/suggestions/distance/<int:event_id>:<string:place_type>",
                      methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_distance(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average distance
    as-the-crow-flies for event members.
    :param event_id: event to request suggestions for
    :param place_type: type of place
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(request_id, event_id,
                                         place_type, "distance")
    return jsonify({"data": result}), 200

@suggestions_bp.route("/suggestions/transit/<int:event_id>:<string:place_type>",
                      methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_transit(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, using public transport.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(request_id, event_id,
                                         place_type, "transit")
    return jsonify({"data": result}), 200

@suggestions_bp.route("/suggestions/drive/<int:event_id>:<string:place_type>",
                      methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_driving(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, driving.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(request_id, event_id,
                                         place_type, "driving")
    return jsonify({"data": result}), 200

@suggestions_bp.route("/suggestions/walk/<int:event_id>:<string:place_type>",
                      methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_walking(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, walking.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(request_id, event_id,
                                         place_type, "walking")
    return jsonify({"data": result}), 200

@suggestions_bp.route("/suggestions/cycle/<int:event_id>:<string:place_type>",
                      methods=["GET"])
@flask_jwt_extended.jwt_required
def suggestions_bicycling(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, cycling.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: HTTP response
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(request_id, event_id,
                                         place_type, "bicycling")
    return jsonify({"data": result}), 200

import flask_jwt_extended
from flask import Blueprint, jsonify, request

from convergence.utils import validators
from convergence.core import events
from convergence.core import invites

events_bp = Blueprint("events", __name__)


@events_bp.route("/events", methods=["POST"])
@flask_jwt_extended.jwt_required
@validators.contains_json_keys(["event_name", "event_date"])
def create_event():
    """
    Create new event, owned by current user
    :param name: event name
    :return: new event info
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    event_name = request.get_json()["event_name"]
    event_date = request.get_json()["event_date"]
    result = events.create_event(user_id, event_name, event_date)
    return jsonify({"data": result}), 200


@events_bp.route("/events/<int:event_id>", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_event(event_id):
    """
    Delete event (requesting user must be event owner)
    :param event_id: event to be deleted
    :return: success status
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    events.delete_event(user_id, event_id)
    return jsonify({"success": True}), 200


@events_bp.route("/events/owned", methods=["GET"])
@flask_jwt_extended.jwt_required
def owned_events():
    """
    Get events owned by user
    :return: event info for all owned events
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = events.get_owned_events(user_id)
    return jsonify({"data": result}), 200


@events_bp.route("/events/invites", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_invites():
    """
    Get pending invitations for current user
    :return: pending invitations
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = invites.get_invites(request_id)
    return jsonify({"data": result}), 200


@events_bp.route("/events/<int:event_id>/<int:user_id>", methods=["POST"])
@flask_jwt_extended.jwt_required
def invite_user_to_event(event_id, user_id):
    """
    Invite user to event (requesting user must be event owner)
    :param event_id: event to invite user to
    :param user_id: user to invite to event
    :return: success status
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    invites.invite_user_to_event(request_id, user_id, event_id)
    return jsonify({"success": True}), 200


@events_bp.route("/events/bulk_invite", methods=["POST"])
@flask_jwt_extended.jwt_required
@validators.contains_json_keys(["event_id", "emails"])
def invite_users_to_event(event_id):
    """
    Invite multiple users to an event (requesting user must be event owner)
    :param event_id: event to invite user to
    :param email: users emails to invite to an event
    :return: success status
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    event_id = request.get_json()["event_id"]
    emails = request.get_json()["emails"]
    not_invited = invites.invite_users_to_event(
        request_id,
        emails,
        event_id
    )
    return jsonify({"data": {"not_invited": list(not_invited)}}), 200


@events_bp.route("/events/invites/<int:invite_id>/accept", methods=["POST"])
@flask_jwt_extended.jwt_required
def accept_invite(invite_id):
    """
    Accept specified pending invite
    :return: event info for accepted invite
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = invites.respond_to_invite(request_id, invite_id, True)
    return jsonify({"data": result}), 200


@events_bp.route("/events/invites/<int:invite_id>/reject", methods=["POST"])
@flask_jwt_extended.jwt_required
def reject_invite(invite_id):
    """
    Reject specified pending invite
    :return: success status
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    invites.respond_to_invite(request_id, invite_id, False)
    return jsonify({"success": True}), 200


@events_bp.route("/events/<int:event_id>/<int:user_id>", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def remove_user_from_event(event_id, user_id):
    """
    Remove user from event (requesting user must be event owner) or
    leave event (if request_id == user_id).
    :param event_id: event to remove user from
    :param user_id: user to remove from event
    :return: success status
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    if request_id == user_id:
        events.leave_event(request_id, event_id)
    else:
        events.remove_user_from_event(request_id, user_id, event_id)
    return jsonify({"success": True}), 200


@events_bp.route("/events/<int:event_id>", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_members(event_id):
    """
    Get list of event members (requesting user must be event member)
    :param event_id: event to request members from
    :return: basic info for all members of event
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = events.get_members(user_id, event_id)
    return jsonify({"data": result}), 200


@events_bp.route("/events", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_events():
    """
    Get events of which requesting user is a member.
    :return: event info for all user's events
    """
    user_id = flask_jwt_extended.get_jwt_identity()
    result = events.get_events(user_id)
    return jsonify({"data": result}), 200

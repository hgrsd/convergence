import flask_jwt_extended
from flask import Blueprint, jsonify, request

from convergence.utils import validators
from convergence.core import friends

friends_bp = Blueprint("friends", __name__)


@friends_bp.route("/friends/invites", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_friend_invites():
    """
    Get pending friend invitations for current user
    :return: pending invitations
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = friends.get_invites(request_id)
    return jsonify({"data": result}), 200


@friends_bp.route("/friends", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_friendships():
    """
    Get friendships for current user
    :return: friendships
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = friends.get_friendships(request_id)
    return jsonify({"data": result}), 200


@friends_bp.route("/friends/<int:user_id>", methods=["POST"])
@flask_jwt_extended.jwt_required
def propose_friendship(user_id):
    request_id = flask_jwt_extended.get_jwt_identity()
    result = friends.propose_friendship(request_id, user_id)
    return jsonify({"data": result}), 200


@friends_bp.route("/friends/bulk_add", methods=["POST"])
@flask_jwt_extended.jwt_required
@validators.contains_json_keys(["emails"])
def propose_friendships():
    """
    Invite multiple users to become friends
    :param email: users emails to invite
    :return: success status
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    not_invited = friends.propose_friendships(
        request_id,
        request.get_json()["emails"],
    )
    return jsonify({"data": {"not_invited": list(not_invited)}}), 200


@friends_bp.route("/friends/invites/<int:invite_id>/accept", methods=["POST"])
@flask_jwt_extended.jwt_required
def accept_friend_invite(invite_id):
    """
    Accept specified pending invite
    :return: friendship info
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = friends.respond_to_invite(
        request_id,
        invite_id,
        True
    )
    return jsonify({"data": result}), 200


@friends_bp.route("/friends/invites/<int:invite_id>/reject", methods=["POST"])
@flask_jwt_extended.jwt_required
def reject_friend_invite(invite_id):
    """
    Reject specified pending invite
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = friends.respond_to_invite(
        request_id,
        invite_id,
        False
    )
    return jsonify({"data": result}), 200


@friends_bp.route("/friends/<int:friend_id>", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_friend(friend_id):
    """
    Remove friend
    :param friend_id: friend to remove
    :return: success status
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    friends.delete_friendship(request_id, friend_id)
    return jsonify({"success": True}), 200

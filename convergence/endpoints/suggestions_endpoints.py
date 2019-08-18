import flask_jwt_extended
from flask import Blueprint, jsonify

from convergence.core import suggestions

suggestions_bp = Blueprint("suggestions", __name__)


@suggestions_bp.route(
    "/events/<int:event_id>/<string:place_type>/distance",
    methods=["GET"]
)
@flask_jwt_extended.jwt_required
def suggestions_distance(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average distance
    as-the-crow-flies for event members.
    :param event_id: event to request suggestions for
    :param place_type: type of place
    :return: list of Places ordered by avg distance
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(
        request_id,
        event_id,
        place_type,
        "distance"
    )
    return jsonify({"data": result}), 200


@suggestions_bp.route(
    "/events/<int:event_id>/<string:place_type>/transit",
    methods=["GET"]
)
@flask_jwt_extended.jwt_required
def suggestions_transit(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, using public transport.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: list of Places ordered by avg transit time
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(
        request_id,
        event_id,
        place_type,
        "transit"
    )
    return jsonify({"data": result}), 200


@suggestions_bp.route(
    "/events/<int:event_id>/<string:place_type>/drive",
    methods=["GET"]
)
@flask_jwt_extended.jwt_required
def suggestions_driving(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, driving.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: list of Places ordered by avg driving time
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(
        request_id,
        event_id,
        place_type,
        "driving"
    )
    return jsonify({"data": result}), 200


@suggestions_bp.route(
    "/events/<int:event_id>/<string:place_type>/walk",
    methods=["GET"]
)
@flask_jwt_extended.jwt_required
def suggestions_walking(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, walking.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: list of Places ordered by avg walking time
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(
        request_id,
        event_id,
        place_type,
        "walking"
    )
    return jsonify({"data": result}), 200


@suggestions_bp.route(
    "/events/<int:event_id>/<string:place_type>/cycle",
    methods=["GET"]
)
@flask_jwt_extended.jwt_required
def suggestions_bicycling(event_id, place_type):
    """
    Get meeting place suggestions based on lowest average travel time for event
    members, cycling.
    :param event_id: event to request suggestions for
    :param place_type: type of places
    :return: list of Places ordered by avg cycling time
    """
    request_id = flask_jwt_extended.get_jwt_identity()
    result = suggestions.get_suggestions(
        request_id,
        event_id,
        place_type,
        "bicycling"
    )
    return jsonify({"data": result}), 200

from . import db
from .events import get_members
from .models import User
from .location import find_centroid, mean_dist_from_centroid
from .places import get_places_around_centroid, order_places_by_travel_time, \
                    order_places_by_distance, sift_places_by_rating


def get_suggestions(request_id, event_id, place_type, suggestions_mode):
    """
    Calculate meeting place suggestions of place_type for an event, based on
    requested suggestion mode.
    :param request_id: requesting user
    :param event_id: event
    :param place_type: type of place to suggest
    :param suggestions_mode: suggestions mode (e.g. "distance" or "transit")
    :return: list of places in requested order (e.g. distance, transit time)
    """
    event_members = get_members(request_id, event_id)
    user_coordinates = [db.session.query(User).get(member["id"]).get_location()
                        for member in event_members]
    centroid = find_centroid(user_coordinates)
    dist_from_centroid = mean_dist_from_centroid(user_coordinates, centroid)
    radius = int(dist_from_centroid / 4)
    places = get_places_around_centroid(centroid, radius, place_type)
    places = sift_places_by_rating(places)
    if not places:
        return []
    if suggestions_mode == "distance":
        ordered_places = order_places_by_distance(user_coordinates, places)
    else:
        ordered_places = order_places_by_travel_time(user_coordinates,
                                                     places,
                                                     suggestions_mode)
    return ordered_places

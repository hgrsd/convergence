from .events import get_available_members
from .models import User
from .location import find_centroid, mean_dist_from_centroid
from .places import get_places_around_centroid, order_places_by_travel_time, \
                    order_places_by_distance, sift_places_by_rating


def get_suggestions(request_id, event_id, place_type, suggestions_mode):
    """
    Calculate meeting place suggestions of place_type for a event, based on
    specified mode of suggestions.
    :param request_id: requesting user
    :param event_id: specified event
    :param place_type: type of place to suggest
    :param suggestions_mode: suggestions mode (e.g. "distance" or "walking")
    :return: tuple(object with suggestions / status message, status code)
    """
    event_members = get_available_members(request_id, event_id)["body"]["data"]
    user_coordinates = [User.query.get(member["id"]).get_location()
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

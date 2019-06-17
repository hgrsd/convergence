from .groups import get_available_members
from .models import User
from .location import find_centroid, mean_dist_from_centroid
from .places import get_places_around_centroid, order_places_by_travel_time, \
                    order_places_by_distance, sift_places_by_rating


def get_suggestions(request_id, group_id, place_type, suggestions_mode):
    """
    Calculate meeting place suggestions of place_type for a group, based on
    specified mode of suggestions.
    :param request_id: requesting user
    :param group_id: specified group
    :param place_type: type of place to suggest
    :param suggestions_mode: suggestions mode (e.g. "distance", "walking", "driving")
    :return: tuple(object with suggestions / status message, status code)
    """
    group_members = get_available_members(request_id, group_id)['body']['data']
    user_coordinates = [User.query.get(member['id']).get_location() for member in group_members]
    centroid = find_centroid(user_coordinates)
    dist_from_centroid = mean_dist_from_centroid(user_coordinates, centroid)
    radius = int(dist_from_centroid / 4)
    places = get_places_around_centroid(centroid, radius, place_type)
    places = sift_places_by_rating(places)
    if not places:
        return {"body": {"status": "success", "data": []}, "status_code": 200}
    if suggestions_mode == "distance":
        ordered_places = order_places_by_distance(user_coordinates, places)
    else:
        ordered_places = order_places_by_travel_time(user_coordinates, places, suggestions_mode)
    return {"body": {"status": "success", "data": ordered_places}, "status_code": 200}



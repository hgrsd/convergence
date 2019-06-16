from .groups import get_available_members
from .location import get_coordinates, find_centroid, mean_dist_from_centroid
from .places import get_places_around_centroid, order_places_by_travel_time, order_places_by_distance


def get_suggestions(request_id, group_id, place_type, suggestions_mode):
    group_members = get_available_members(request_id, group_id)[0]
    user_coordinates = [get_coordinates(member['id']) for member in group_members['data']]
    centroid = find_centroid(user_coordinates)
    dist_from_centroid = mean_dist_from_centroid(user_coordinates, centroid)
    radius = int(dist_from_centroid / 4)
    places = get_places_around_centroid(centroid, radius, place_type)
    if not places:
        return {"status": "success", "data": []}, 200
    if suggestions_mode == "distance":
        ordered_places = order_places_by_distance(user_coordinates, places)
    else:
        ordered_places = order_places_by_travel_time(user_coordinates, places, suggestions_mode)
    return {"status": "success", "data": ordered_places}, 200



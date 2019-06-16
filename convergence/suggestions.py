from .groups import get_available_members
from .location import get_coordinates, find_centroid
from .places import get_places_around_centroid, order_places_by_travel_time, order_places_by_distance


def get_suggestions(request_id, group_id, place_type, suggestions_mode):
    group_members = get_available_members(request_id, group_id)[0]
    user_coordinates = [get_coordinates(member['id']) for member in group_members['data']]
    centroid = find_centroid(user_coordinates)
    places = get_places_around_centroid(centroid, 1500, place_type)
    if suggestions_mode == "distance":
        order = order_places_by_distance(user_coordinates, places)
    else:
        order = order_places_by_travel_time(user_coordinates, places, suggestions_mode)
    ordered_places = []
    for x in range(len(order)):
        place = places[order[x][0]]
        total = order[x][1]
        mode_string = "total_distance" if suggestions_mode == "distance" else "total_travel_time"
        ordered_places.append({"place": place, mode_string: total})
    return {"status": "success", "data": ordered_places}, 200



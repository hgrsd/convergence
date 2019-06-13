import math
from flask import jsonify
from .groups import get_members
from .location import get_coordinates
from .places import get_places_around_centroid, order_by_travel_time


def get_suggestions(request_id, group_id, place_type):
    group_members = get_members(request_id, group_id)
    user_coordinates = [get_coordinates(member['user_id']) for member in group_members]
    centroid = find_centroid(user_coordinates)
    places = get_places_around_centroid(*centroid, 600, place_type)
    order = order_by_travel_time(user_coordinates, places, "transit")
    ordered_places = []
    for x in range(len(order)):
        place = places[order[x][0]]
        total_time = order[x][1]
        ordered_places.append({"place": place, "total_travel_time": total_time})
    return jsonify({"status": "success", "data": ordered_places})


def find_centroid(coordinates):
    x_total, y_total, z_total = 0, 0, 0
    for coordinate in coordinates:
        lat = math.radians(float(coordinate[0]))
        lon = math.radians(float(coordinate[1]))
        x_total += math.cos(lat) * math.cos(lon)
        y_total += math.cos(lat) * math.sin(lon)
        z_total += math.sin(lat)
    x = float(x_total / len(coordinates))
    y = float(y_total / len(coordinates))
    z = float(z_total / len(coordinates))
    return math.degrees(math.atan2(z, math.sqrt(x * x + y * y))), math.degrees(math.atan2(y, x))

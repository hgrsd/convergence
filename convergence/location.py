from .models import User
from . import db
import math


class Point:
    
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def __str__(self):
        return f"{self.lat}, {self.long}"

    def distance_to(self, other):
        self_lat = math.radians(self.lat)
        self_long = math.radians(self.long)
        other_lat = math.radians(other.lat)
        other_long = math.radians(other.long)
        R = 6371
        dist = math.acos(math.sin(self_lat) * math.sin(other_lat)
                         + math.cos(self_lat) * math.cos(other_lat)
                         * math.cos(self_long - other_long)) * R
        return dist * 1000  # return distance in metres


def update_location(user_id, lat, long):
    user = User.query.filter_by(id=user_id).first()
    user.last_seen_lat, user.last_seen_long = lat, long
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"error": {"message": "error updating location"}}, 400
    return {"status": "success"}, 200


def get_coordinates(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    else:
        return Point(user.last_seen_lat, user.last_seen_long)


def find_centroid(coordinates):
    x_total, y_total, z_total = 0, 0, 0
    for coordinate in coordinates:
        lat = math.radians(float(coordinate.lat))
        lon = math.radians(float(coordinate.long))
        x_total += math.cos(lat) * math.cos(lon)
        y_total += math.cos(lat) * math.sin(lon)
        z_total += math.sin(lat)
    x = float(x_total / len(coordinates))
    y = float(y_total / len(coordinates))
    z = float(z_total / len(coordinates))
    return Point(math.degrees(math.atan2(z, math.sqrt(x * x + y * y))), math.degrees(math.atan2(y, x)))


def mean_dist_from_centroid(coordinates, centroid):
    dist = sum(coordinate.distance_to(centroid) for coordinate in coordinates)
    return dist / len(coordinates)


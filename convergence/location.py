import math

from .point import Point

MIN_LAT = -90.0
MAX_LAT = 90.0
MIN_LON = -180.0
MAX_LON = 180.0


def find_centroid(coordinates):
    """
    Find centroid of list of coordinates
    :param coordinates: list of coordinates as Points
    :return: centroid as Point
    """
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
    return Point(math.degrees(math.atan2(z, math.sqrt(x * x + y * y))),
                 math.degrees(math.atan2(y, x)))


def mean_dist_from_centroid(coordinates, centroid):
    """
    Calculate mean distance between centroid and list of coordinates
    :param coordinates: list of coordinates as Points
    :param centroid: centroid as Point
    :return: mean distance between centroid and coordinates in metres
    """
    dist = sum(coordinate.distance_to(centroid) for coordinate in coordinates)
    return dist / len(coordinates)

import math

from convergence.core import location


class Point:
    """ Point class, used for coordinates"""
    def __init__(self, lat, long):
        try:
            self.lat = float(lat)
            self.long = float(long)
        except ValueError:
            raise TypeError("Coordinates must be numerical.")
        if not location.MIN_LAT <= self.lat <= location.MAX_LAT or \
           not location.MIN_LON <= self.long <= location.MAX_LON:
            raise ValueError("Invalid location coordinates.")

    def __str__(self):
        return f"{self.lat:.6f}, {self.long:.6f}"

    def __eq__(self, other):
        return self.lat == other.lat and self.long == other.long

    def distance_to(self, other):
        """
        Return distance between this and other Point
        :param other: other Point
        :return: distance in metres
        """
        self_lat = math.radians(self.lat)
        self_long = math.radians(self.long)
        other_lat = math.radians(other.lat)
        other_long = math.radians(other.long)
        R = 6371
        dist = math.acos(
            math.sin(self_lat) * math.sin(other_lat)
            + math.cos(self_lat) * math.cos(other_lat)
            * math.cos(self_long - other_long)
        ) * R

        return dist * 1000

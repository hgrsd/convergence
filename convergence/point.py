import math


class Point:
    """ Point class, used for coordinates"""
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def __str__(self):
        return f"{self.lat}, {self.long}"

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
        dist = math.acos(math.sin(self_lat) * math.sin(other_lat)
                         + math.cos(self_lat) * math.cos(other_lat)
                         * math.cos(self_long - other_long)) * R
        return dist * 1000

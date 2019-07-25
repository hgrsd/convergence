from datetime import datetime

from convergence import gmaps_api
from convergence import duration
from convergence.models import Place
from convergence.location import Point
from convergence.repo import PlaceStore, DurationStore

MIN_PLACES_FROM_DATABASE = 4


place_store = PlaceStore()
duration_store = DurationStore()


def get_places_around_centroid(point, radius, place_type):
    """
    Find places of place_type within a radius around a centroid
    and add to database.
    :param point: the centroid, of type Point
    :param radius: radius (in metres)
    :param place_type: type of place to be searched for
    :return: list of places around centroid
    """
    places_query = place_store.get_places_around_point(point, radius)
    if len(places_query) >= MIN_PLACES_FROM_DATABASE:
        return [p.as_dict() for p in places_query if place_type in p.gm_types]
    places_ids = {place["gm_id"] for place in places_query}
    places = gmaps_api.get_places_around_point(point, radius, place_type)
    for place in places:
        if place["gm_id"] not in places_ids:
            place_store.add_place(
                Place(
                    name=place["name"],
                    gm_id=place["gm_id"],
                    lat=place["lat"],
                    long=place["long"],
                    address=place["address"],
                    gm_price=place["price_level"],
                    gm_rating=place["gm_rating"],
                    gm_types=place["types"],
                    timestamp=datetime.utcnow()
                )
            )
    return places


def add_distance_to_places(user_coordinates, places):
    """
    Calculate distance between each user and each place, add them
    up to calculate total distance for each place.
    :param user_coordinates: list of Points for relevant users
    :param places: list of places
    :return: list of places with added travel_total key
    """
    places_coordinates = [
        Point(place["lat"], place["long"]) for place in places
    ]
    for place in places:
        place["travel_total"] = 0
    for user in user_coordinates:
        for i, place in enumerate(places_coordinates):
            places[i]["travel_total"] += user.distance_to(place)
    return places


def add_travel_time_to_places(user_coordinates, places, mode):
    """
    Return all places with total travel time added for each place.

    :param user_coordinates: list of Points for relevant users
    :param places: list of places (dicts)
    :param mode: mode of transportation
    :return: list of places with added travel_total key
    """
    return duration.add_duration_to_places(user_coordinates, places, mode)

def sort_places_by_travel_total(places):
    return sorted(places, key=lambda x: x["travel_total"])


def sort_places_by_rating(places):
    """
    Return list of places, sorted by ranking (highest to lowest)
    :param places: list of places
    :return: list of places, sorted by rating
    """
    for place in places:
        if not place["gm_rating"]:
            place["gm_rating"] = 1
    places = sorted(places, key=lambda x: x["gm_rating"], reverse=True)
    return places

from datetime import datetime

from . import gmaps_api
from .models import Place
from .location import Point
from .repositories import PlaceStore

MIN_PLACES_FROM_DATABASE = 4
MAX_PLACES_PER_SUGGESTION = 10

place_store = PlaceStore()


def get_places_around_centroid(point, radius, place_type):
    """
    Find places of place_type within a radius around a centroid
    and add to database.
    :param point: the centroid, of type Point
    :param radius: radius (in metres)
    :param place_type: type of place to be searched for
    :return: list of places aroind centroid
    """
    places_query = place_store.get_places_around_point(point, radius)
    places = [place.as_dict() for place in places_query
              if place_type in place.gm_types]
    if len(places) < MIN_PLACES_FROM_DATABASE:
        places = gmaps_api.places_around_point(point, radius, place_type)
        for place in places:
            new_record = Place(name=place["name"], gm_id=place["gm_id"],
                               lat=place["lat"], long=place["long"],
                               address=place["address"],
                               gm_price=place["price_level"],
                               gm_rating=place["gm_rating"],
                               gm_types=place["types"],
                               timestamp=datetime.utcnow())
            place_store.add_place(new_record)
    if len(places) > MAX_PLACES_PER_SUGGESTION:
        places = sort_places_by_rating(places)[:MAX_PLACES_PER_SUGGESTION]
    return places


def order_places_by_distance(user_coordinates, places):
    """
    Return places sorted in ascending order by the sum of their distances
    to each user.
    :param user_coordinates: list of Points for relevant users
    :param places: list of places to be ordered
    :return: list of places in ascending order, with travel_total
            added as key for each place
    """
    places_coordinates = [Point(place["lat"], place["long"])
                          for place in places]
    for place in places:
        place["travel_total"] = 0
    for user in user_coordinates:
        for i, place in enumerate(places_coordinates):
            places[i]["travel_total"] += user.distance_to(place)
    ordered_places = sorted(places, key=lambda x: x["travel_total"])
    return ordered_places


def order_places_by_travel_time(user_coordinates, places, mode):
    """
    Return places sorted in ascending order by the sum of the travel time,
    using specified mode of travel, from each user to each place.
    :param user_coordinates: list of Points for relevant users
    :param places: list of places to be ordered
    :param mode: mode of transportation
    :return: sorted list of places with travel_total added
            as key for each place
    """
    places_coordinates = [Point(place["lat"],
                          place["long"]) for place in places]
    dist_matrix = gmaps_api.distance_matrix(user_coordinates,
                                            places_coordinates,
                                            mode)
    for place in places:
        place["travel_total"] = 0
    for row in dist_matrix:
        for i, place in enumerate(row):
            places[i]["travel_total"] += place["duration"]["value"]
    ordered_places = sorted(places, key=lambda x: x["travel_total"])
    return ordered_places


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

from sqlalchemy import exc
from datetime import datetime

from . import db
from . import gmaps_api
from .models import Place
from .location import Point

MAX_PLACES = 10

def get_places_around_centroid(point, radius, place_type):
    """
    Find places of place_type within a radius around a centroid and add to database.
    :param point: the centroid, of type Point
    :param radius: radius (in metres)
    :param place_type: type of place to be searched for
    :return: list of places (as dicts)
    """
    places_query = Place.query.filter(Place.within_range(point, radius))
    places = [place.as_dict() for place in places_query if place_type in place.gm_types]
    if len(places) < 0.25 * MAX_PLACES:
        places = gmaps_api.places_around_point(point, radius, place_type)
        for place in places:
            place_entry = Place(name=place["name"], gm_id=place["gm_id"],
                                lat=place["lat"], long=place["long"],
                                address=place["address"], gm_price=place["price_level"],
                                gm_rating=place["gm_rating"], gm_types=place["types"],
                                timestamp=datetime.utcnow())
            db.session.add(place_entry)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
    return places


def order_places_by_distance(user_coordinates, places):
    """
    Return places sorted in ascending order by the sum of their distances to each user.
    :param user_coordinates: list of Points for relevant users
    :param places: list of places (as dicts) to be ordered
    :return: list of places (as dicts) in ascending order, with travel_total
            added as key for each place
    """
    places_coordinates = [Point(place["lat"], place["long"]) for place in places]
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
    :param places: list of places (as dicts) to be ordered
    :param mode: mode of transportation, as string
    :return: sorted list of places (as dicts)with travel_total added
            as key for each place
    """
    places_coordinates = [Point(place["lat"], place["long"]) for place in places]
    dist_matrix = gmaps_api.distance_matrix(user_coordinates, places_coordinates, mode)
    for place in places:
        place["travel_total"] = 0
    for row in dist_matrix:
        for i, place in enumerate(row):
            places[i]["travel_total"] += place["duration"]["value"]
    ordered_places = sorted(places, key=lambda x: x["travel_total"])
    return ordered_places


def sift_places_by_rating(places):
    """
    Return MAX_PLACES-length list of places, sorted by rating in descending order
    if len(places) > MAX_PLACES
    :param places: list of places (as dict)
    :return: MAX_PLACES-length list of places (as dict), sorted by rating
    """
    if len(places) < MAX_PLACES:
        return places
    else:
        for place in places:
            if not place["gm_rating"]:
                place["gm_rating"] = 1
        places = sorted(places, key=lambda x: x["gm_rating"], reverse=True)
        return places[:MAX_PLACES]

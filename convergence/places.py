from .models import Place
from . import db
from . import gmaps_api
from .location import Point
from sqlalchemy import exc
from datetime import datetime

MAX_PLACES = 5


def get_places_around_centroid(point, radius, place_type):
    places_query = Place.query.filter(Place.within_range(point, radius))
    places = [place.as_dict() for place in places_query if place_type in place.gm_types]
    if len(places) == 0:
        places = gmaps_api.places_around_point(point, radius, place_type)
        for place in places:
            place_entry = Place(name=place['name'], gm_id=place['gm_id'],
                                lat=place['lat'], long=place['long'],
                                address=place['address'], gm_price=place['price_level'],
                                gm_rating=place['gm_rating'], gm_types=place['types'],
                                timestamp=datetime.utcnow())
            db.session.add(place_entry)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
    # return a list of MAX_PLACES length, based on rating
    return sift_places_by_rating(places)


def order_places_by_distance(user_coordinates, places):
    places_coordinates = [Point(place['lat'], place['long']) for place in places]
    total_travel = {}
    for x in range(len(places)):
        total_travel[x] = 0
    for user in user_coordinates:
        for i, place in enumerate(places_coordinates):
            total_travel[i] += user.distance_to(place)
    order = (sorted(total_travel.items(), key=lambda x: x[1]))
    return order


def order_places_by_travel_time(user_coordinates, places, mode):
    places_coordinates = [Point(place['lat'], place['long']) for place in places]
    dist_matrix = gmaps_api.distance_matrix(user_coordinates, places_coordinates, mode)
    total_travel = {}
    for x in range(len(places)):
        total_travel[x] = 0
    for row in dist_matrix:
        for i, place in enumerate(row):
            total_travel[i] += place['duration']['value']
    order = (sorted(total_travel.items(), key=lambda x: x[1]))
    return order


def sift_places_by_rating(places):
    if len(places) < MAX_PLACES:
        return places
    else:
        for place in places:
            if not place['gm_rating']:
                place['gm_rating'] = 1
        places = sorted(places, key=lambda x: x['gm_rating'], reverse=True)
        return places[:MAX_PLACES]
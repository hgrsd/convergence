from .models import Place
from . import db
from . import gmaps_api
from sqlalchemy import exc


def get_places_around_centroid(lat, long, radius, place_type):
    places = gmaps_api.places_around_point(lat, long, radius, place_type)
    for place in places:
        place_entry = Place(name=place['name'], gm_id=place['gm_id'],
                            lat=place['lat'], long=place['long'],
                            address=place['address'], gm_price=place['price_level'],
                            gm_rating=place['rating'], gm_types=place['types'])
        db.session.add(place_entry)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
    return places


def order_by_travel_time(user_coordinates, places, mode):
    places_coordinates = [(place['lat'], place['long']) for place in places]
    dist_matrix = gmaps_api.distance_matrix(user_coordinates, places_coordinates, mode)
    total_travel = {}
    for x in range(len(places)):
        total_travel[x] = 0
    for row in dist_matrix:
        for i, place in enumerate(row):
            total_travel[i] += place['duration']['value']
    order = (sorted(total_travel.items(), key=lambda x: x[1]))
    return order

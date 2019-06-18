import requests
import time
import math

from urllib.parse import quote
from . import app

GM_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={:f},{:f}&radius={:d}&type={:s}&key={:s}"
GM_TRAVEL_TIME_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={:s}&destinations={:s}&mode={:s}&key={:s}"
GM_API_KEY = app.config.get("GM_API_KEY")
DISTANCE_MATRIX_MAX_ELEMENTS = 100


def places_around_point(point, radius, place_type):
    """
    Find, using Google Nearby Places API, all places of place_type within
    specified radius from point
    :param point: centre point, type Point
    :param radius: radius in metres
    :param place_type: place type to find
    :return: list of places (as dicts)
    """
    init_request = GM_PLACES_URL.format(point.lat, point.long, radius, place_type, GM_API_KEY)
    response = requests.get(init_request).json()
    places = _json_extract_places(response)
    while "next_page_token" in response:
        time.sleep(1.5)
        request = init_request + "&pagetoken=" + quote(response["next_page_token"])
        response = requests.get(request).json()
        places.extend(_json_extract_places(response))
    return places


def distance_matrix(origins, destinations, mode):
    """
    Use Google Distance Matrix API to request distance matrix between origins
    and destinations, using specified mode of transportation
    :param origins: list of Points
    :param destinations: list of Points
    :param mode: mode of transportation
    :return: distance matrix of dimension len(origins) * len(destinations)
    """
    no_requests = math.ceil(len(origins) * len(destinations) / DISTANCE_MATRIX_MAX_ELEMENTS)
    matrix = [None] * len(origins)
    for i in range(no_requests):
        start = 0 + i * (len(destinations) // no_requests)
        cutoff = len(destinations) // no_requests * (i + 1)
        locations_string = ""
        for origin in origins:
            if locations_string != "":
                locations_string += "|"
            locations_string = locations_string + str(origin.lat) + "," + str(origin.long)
        places_string = ""
        for destination in destinations[start:cutoff]:
            if places_string != "":
                places_string += "|"
            places_string = places_string + str(destination.lat) + "," + str(destination.long)
        request = GM_TRAVEL_TIME_URL.format(quote(locations_string),
                                            quote(places_string),
                                            mode,
                                            GM_API_KEY)
        response = requests.get(request).json()
        for i, row in enumerate(response["rows"]):
            if not matrix[i]:
                matrix[i] = row["elements"]
            else:
                matrix[i].extend(row["elements"])
        if no_requests > 1:
            time.sleep(2)
    return matrix


def _json_extract_places(response_string):
    """
    Extract place information from Google Places API JSON object.
    :param response_string: response JSON object
    :return: list of places (as dict)
    """
    places = []
    for result in response_string["results"]:
        if "permanently_closed" in result:
            continue
        lat = result["geometry"]["location"]["lat"]
        long = result["geometry"]["location"]["lng"]
        name = result["name"]
        types = result["types"]
        address = result["vicinity"]
        gm_id = result["place_id"]
        try:
            price_level = result["price_level"]
        except KeyError:
            price_level = None
        try:
            rating = result["rating"]
        except KeyError:
            rating = None
        places.append({"name": name, "gm_id": gm_id, "lat": lat, "long": long, "address": address,
                       "types": types, "price_level": price_level, "gm_rating": rating})
    return places

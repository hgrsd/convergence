import requests
import time
import math
from urllib.parse import quote

from convergence import app
from convergence.utils import logger
from convergence.utils.exceptions import ServerError

GM_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/" \
                "json?location={:f},{:f}&radius={:d}&type={:s}&key={:s}"
GM_TRAVEL_TIME_URL = "https://maps.googleapis.com/maps/api/distancematrix/" \
                     "json?origins={:s}&destinations={:s}&mode={:s}&key={:s}"
GM_API_KEY = app.config.get("GM_API_KEY")

DISTANCE_MATRIX_MAX_ELEMENTS = 100


def get_places_around_point(point, radius, place_type):
    """
    Find, using Google Nearby Places API, all places of place_type within
    specified radius from point.
    :param point: centre point, type Point
    :param radius: radius in metres
    :param place_type: place type to find
    :return: list of places around point
    """
    base_request = GM_PLACES_URL.format(
        point.lat,
        point.long,
        radius,
        place_type,
        GM_API_KEY
    )
    response = requests.get(base_request).json()
    if not response:
        logger.log_error(
            f"Invalid response from Google API. Request URL: {base_request}"
        )
        raise ServerError("Unable to reach Google Maps API (Places).")
    places = _json_extract_places(response)
    while "next_page_token" in response:
        time.sleep(1)
        response = requests.get(
            base_request + "&pagetoken=" + quote(response["next_page_token"])
        ).json()
        if not response:
            logger.log_error(
                f"Invalid response from Google API. Request URL: {base_request}"
            )
            raise ServerError("Unable to reach Google Maps API (Places).")
        places.extend(_json_extract_places(response))
    return places


def get_distance_matrix(origins, destinations, mode):
    """
    Use Google Distance Matrix API to request distance matrix between origins
    and destinations, using specified mode of transportation.

    Given that Google Distance Matrix API is limited in the number of elements
    it can return in any single request, this function calculates how many
    requests are needed to include all elements of the matrix with size
    (origins * destinations), and places multiple requests if needed.

    :param origins: list of origin Points
    :param destinations: list of destination Points
    :param mode: mode of transportation
    :return: distance matrix of dimension len(origins) * len(destinations)
    """
    dist_matrix = [[None] * len(destinations) for _ in range(len(origins))]

    no_requests = math.ceil(
        len(origins) * len(destinations) / DISTANCE_MATRIX_MAX_ELEMENTS
    )
    start = 0
    for i in range(no_requests):
        cutoff = min(
            start + math.ceil(len(destinations) / no_requests),
            len(destinations)
        )
        origins_list = [
            ",".join([str(origin.lat), str(origin.long)])  # stringify coords
            for origin in origins
        ]
        dest_list = [
            ",".join([str(dest.lat), str(dest.long)])
            for dest in destinations[start:cutoff]
        ]
        request = GM_TRAVEL_TIME_URL.format(
            quote("|".join(origins_list)),  # Google format: x1,y1|x2,y2|xn,yn
            quote("|".join(dest_list)),
            mode,
            GM_API_KEY
        )
        response = requests.get(request).json()
        if not response["rows"]:
            logger.log_error(
                f"Invalid response from Google API. Request URL: {request}"
            )
            raise ServerError("Error retrieving distance information")
        for row_idx, row in enumerate(response["rows"]):
            for el_idx, element in enumerate(row["elements"]):
                if element["status"] != "OK":
                    dist_matrix[row_idx][el_idx] = math.inf
                else:
                    dist_matrix[row_idx][el_idx] = element["duration"]["value"]
        if i < no_requests - 1:
            start = cutoff
            time.sleep(1)  # sleep before next request

    return dist_matrix


def _json_extract_places(response_string):
    """
    Extract place information from Google Places API JSON object.
    :param response_string: response JSON object
    :return: list of places with attributes
    """
    places = []
    for result in response_string["results"]:
        if "permanently_closed" in result:
            logger.log_info(
                f"Place permanently closed: {result['place_id']}"
            )
            continue
        try:
            lat = result["geometry"]["location"]["lat"]
            long = result["geometry"]["location"]["lng"]
            name = result["name"]
            types = result["types"]
            address = result["vicinity"]
            gm_id = result["place_id"]
        except KeyError:
            continue
        try:
            price_level = result["price_level"]
        except KeyError:
            price_level = None
        try:
            rating = result["rating"]
        except KeyError:
            rating = None
        places.append(
            {
                "name": name,
                "gm_id": gm_id,
                "lat": lat,
                "long": long,
                "address": address,
                "types": types,
                "price_level": price_level,
                "gm_rating": rating
            }
        )
    return places

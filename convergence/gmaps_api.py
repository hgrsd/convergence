import requests
import time
import math
from urllib.parse import quote
from . import app

GM_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={:f},{:f}&radius={:d}&type={:s}&key={:s}"
GM_TRAVEL_TIME_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={:s}&destinations={:s}&mode={:s}&key={:s}"
GM_API_KEY = app.config.get('GM_API_KEY')


def places_around_point(lat, long, radius, place_type):
    print(lat, long, radius, place_type)
    init_request = GM_PLACES_URL.format(lat, long, radius, place_type, GM_API_KEY)
    response = requests.get(init_request).json()
    places = _json_extract_places(response)
    print(response)
    print(places)
    while "next_page_token" in response:
        time.sleep(1.5)
        request = init_request + "&pagetoken=" + quote(response["next_page_token"])
        print(request)
        response = requests.get(request).json()
        places.extend(_json_extract_places(response))
    return places


def distance_matrix(origins, destinations, mode):
    no_requests = math.ceil(len(origins) * len(destinations) / 100)
    matrix = [None] * len(origins)
    for i in range(no_requests):
        start = 0 + i * (len(destinations) // no_requests)
        cutoff = len(destinations) // no_requests * (i + 1)
        print(start, cutoff)
        locations_string = ""
        for origin in origins:
            if locations_string != "":
                locations_string += "|"
            locations_string = locations_string + str(origin[0]) + "," + str(origin[1])
        places_string = ""
        for destination in destinations[start:cutoff]:
            if places_string != "":
                places_string += "|"
            places_string = places_string + str(destination[0]) + "," + str(destination[1])
        request = GM_TRAVEL_TIME_URL.format(quote(locations_string),
                                            quote(places_string),
                                            mode,
                                            GM_API_KEY)
        response = requests.get(request).json()
        for i, row in enumerate(response['rows']):
            if not matrix[i]:
                matrix[i] = row['elements']
            else:
                matrix[i].extend(row['elements'])
        time.sleep(2)
    return matrix


def _json_extract_places(response_string):
    places = []
    for result in response_string['results']:
        lat = result['geometry']['location']['lat']
        long = result['geometry']['location']['lng']
        name = result['name']
        types = result['types']
        address = result['vicinity']
        gm_id = result['place_id']
        try:
            price_level = result['price_level']
        except KeyError:
            price_level = None
        try:
            rating = result['rating']
        except KeyError:
            rating = None
        places.append({"name": name, "gm_id": gm_id, "lat": lat, "long": long, "address": address,
                       "types": types, "price_level": price_level, "rating": rating})
    return places

import math

from convergence import location
from convergence import places
from convergence import events
from convergence.point import Point
from convergence.repo import UserStore

MEAN_DIST_TO_RADIUS_RATIO = 0.25
MAX_PLACES_PER_SUGGESTION = 10

user_store = UserStore()


def get_suggestions(request_id, event_id, place_type, suggestions_mode):
    """
    Calculate meeting place suggestions of place_type for an event, based on
    requested suggestion mode.
    :param request_id: requesting user
    :param event_id: event
    :param place_type: type of place to suggest
    :param suggestions_mode: suggestions mode (e.g. "distance" or "transit")
    :return: list of places in requested order (e.g. distance, transit time)
    """
    ids = [member["id"] for member in events.get_members(request_id, event_id)]
    users = user_store.get_users_by_ids(ids)
    user_coordinates = [Point(*user.get_location()) for user in users]
    centroid = location.find_centroid(user_coordinates)
    mean_dist = location.mean_dist_from_centroid(
        user_coordinates,
        centroid
    )
    radius = math.ceil(mean_dist * MEAN_DIST_TO_RADIUS_RATIO)
    potential_places = places.get_places_around_centroid(
        centroid,
        radius,
        place_type
    )
    if not potential_places:
        return []
    if len(potential_places) > MAX_PLACES_PER_SUGGESTION:
        potential_places = places.sort_places_by_rating(
            potential_places
        )[:MAX_PLACES_PER_SUGGESTION]
    if suggestions_mode == "distance":
        potential_places = places.add_distance_to_places(
            user_coordinates,
            potential_places
        )
    else:
        potential_places = places.add_travel_time_to_places(
            user_coordinates,
            potential_places,
            suggestions_mode,
        )
    return places.sort_places_by_travel_total(potential_places)

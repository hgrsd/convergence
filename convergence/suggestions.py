import math

from . import location
from . import places
from . import db
from . import events
from .models import User

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
    member_ids = [member["id"] for member
                  in events.get_members(request_id, event_id)]
    users = db.session.query(User).filter(User.id.in_(member_ids)).all()
    user_coordinates = [user.get_location() for user in users]
    centroid = location.find_centroid(user_coordinates)
    dist_from_centroid = location.mean_dist_from_centroid(user_coordinates,
                                                          centroid)
    radius = math.ceil(dist_from_centroid) / 4
    potential_places = places.get_places_around_centroid(centroid,
                                                         radius,
                                                         place_type)
    if not potential_places:
        return []
    sifted_places = places.sift_places_by_rating(potential_places)
    if suggestions_mode == "distance":
        return places.order_places_by_distance(user_coordinates, sifted_places)
    else:
        return places.order_places_by_travel_time(user_coordinates,
                                                  sifted_places,
                                                  suggestions_mode)

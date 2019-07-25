from convergence import gmaps_api
from convergence.repo import DurationStore
from convergence.point import Point

duration_store = DurationStore()


def merge_matrices(dist_matrix, gmaps_matrix):
    """
    Merge the result of an API call into a part-filled dist_matrix
    :param dist_matrix: m*n initialised (and/or part-filled) matrix
    :param gmaps_matrix: m*n API response matrix
    :return merged distance matrix
    """
    gmaps_idx = 0
    for i in range(len(dist_matrix)):
        if dist_matrix[i][0]:
            continue
        else:
            if gmaps_idx < len(gmaps_matrix):
                dist_matrix[i] = gmaps_matrix[gmaps_idx]
                gmaps_idx += 1
    return dist_matrix


def fill_durations_from_store(matrix, users, places, mode, radius):
    """
    Request durations from store. In addition to exact coordinates,
    known points within radius of user locations may be used, too.

    If for a given user (or point close to user) we already know the durations
    to _all_ places, then fill that user's row in the distance matrix from
    store. The user can then be left out from an API call.

    If not, add the user to the to_request list. They will be included as
    an originin the API call to be placed.

    Note that this function fills the given matrix in-place.

    :param matrix: the initialised empty distance matrix to fill
    :param users: a list of user locations (Points)
    :param places: a list of place locations (Points)
    :param mode: travel mode
    :param radius: radius in metres

    :return: A list of users for whom a API call needs to be placed.
    """
    to_request = []
    for i, user in enumerate(users):
        nearby_coords = duration_store.get_nearby_coordinates(
            user,
            mode,
            radius
        )
        if nearby_coords:
            coordinate = Point(*nearby_coords[0])  # take first point
            durations = []
            for j, place in enumerate(places):
                duration = duration_store.get_travel_time(
                    coordinate, place, mode
                )
                if duration:
                    durations.append(duration[0])
            if len(durations) == len(places):  # entire row can be filled
                matrix[i] = durations[:]
            else:
                to_request.append(user)
        else:
            to_request.append(user)
    return to_request


def build_dist_matrix(users, places, mode):
    """
    Build distance matrix users x places based on travel duration
    with specified mode of travel.
    :param users: list of user coordinates (Points)
    :param places: list of place coordinates (Points)
    :param mode: travel mode
    :return: users * places distance matrix
    """
    dist_matrix = [
        [None] * len(places) for _ in range(len(users))
    ]
    to_request = fill_durations_from_store(
        dist_matrix,
        users,
        places,
        mode,
        250  # Radius in metres -- TODO: formula instead of hardcoded
    )
    if to_request:  # place API call if empty rows left
        matrix_from_gmaps = gmaps_api.get_distance_matrix(
            to_request,
            places,
            mode
        )
        dist_matrix = merge_matrices(dist_matrix, matrix_from_gmaps)
    return dist_matrix


def add_duration_to_places(users, places, mode):
    """
    Query store for travel times for each user (or point near user) to
    each place; call google distance matrix if travel times aren't known.

    Return all places with total travel time.

    :param user_coordinates: list of Points for relevant users
    :param places: list of places (as dict)
    :param mode: mode of transportation
    :return: list of places with added travel_total key
    """
    places_coordinates = [
        Point(place["lat"], place["long"]) for place in places
    ]
    dist_matrix = build_dist_matrix(users, places_coordinates, mode)
    for place in places:
        place["travel_total"] = 0  # initialise travel_total to 0
    for user_idx, row in enumerate(dist_matrix):
        for place_idx, col in enumerate(row):
            duration = dist_matrix[user_idx][place_idx]
            places[place_idx]["travel_total"] += duration
            duration_store.update_duration(
                users[user_idx],
                places_coordinates[place_idx],
                duration,
                mode
            )
    return places

from convergence import location
from convergence import exceptions
from convergence import validators
from convergence.models import User
from convergence.repo import UserStore

user_store = UserStore()


def login(email, password):
    """
    Login user
    :return user_id
    """
    user = user_store.get_user_by_email(email)
    if not user or not user.verify_password(password):
        raise exceptions.LoginError("Incorrect email address or password.")
    return user.id


def get_info(user_id):
    """
    Get full info about currently logged in user
    :return full info for current user
    """
    user = user_store.get_user_by_id(user_id)
    if not user:
        raise exceptions.NotFoundError("Invalid user id.")
    return user.full_info()


def register_user(email, password, screen_name, phone):
    """
    Register user.
    :return full info for registered user
    """
    if not 0 < len(screen_name) <= 64:
        raise exceptions.InputError("Invalid screen name")
    if not validators.is_email_format(email):
        raise exceptions.InputError("Invalid email address.")
    if not password:
        raise exceptions.InputError("Invalid password.")
    if phone and not validators.is_phone_format(phone):
        raise exceptions.InputError("Invalid phone number.")
    user = User(
        screen_name=screen_name,
        email=email,
        phone=phone
    )
    user.hash_password(password)
    user_store.add_user(user)
    return user.full_info()


def delete_user(user_id):
    """
    Delete user.
    """
    user = user_store.get_user_by_id(user_id)
    if not user:
        raise exceptions.NotFoundError("Invalid user id.")
    user_store.delete_user(user)
    return None


def find_user(email):
    """
    Return user info for email
    :return basic user info if found
    """
    user = user_store.get_user_by_email(email)
    if not user:
        return []
    else:
        return user.basic_info()


def update_location(user_id, lat, long):
    """
    Update user location in database
    :param user_id: requesting user
    :param lat: new latitude
    :param long: new longitude
    :return: location info
    """
    if not location.MIN_LAT <= lat <= location.MAX_LAT \
            or not location.MIN_LON <= long <= location.MAX_LON:
        raise exceptions.LocationError("Invalid coordinates.")
    user = user_store.get_user_by_id(user_id)
    if not user:
        raise exceptions.NotFoundError("Invalid user id.")
    user.latitude, user.longitude = lat, long
    user_store.commit_changes()
    return user.get_location()

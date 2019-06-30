from sqlalchemy import exc

from . import location
from . import db
from .models import User
from .exceptions import LoginError, AccountError, NotFoundError, \
                        DatabaseError, LocationError


def login(username, password):
    """
    Login user
    :return user_id
    """
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        raise LoginError("Incorrect username or password.")
    return user.id


def get_info(user_id):
    """
    Get full info about currently logged in user
    :return full info for current user
    """
    user = db.session.query(User).get(user_id)
    if not user:
        raise NotFoundError("Invalid user id.")
    return user.full_info()


def register_user(username, password):
    """
    Register user.
    :return full info for registered user
    """
    if not username.isalnum():
        raise AccountError("Username must be alphanumeric.")
    user = User(username=username, available=False)
    user.hash_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        raise AccountError("Username exists already.")
    return user.full_info()


def delete_user(user_id):
    """
    Delete user.
    """
    user = db.session.query(User).get(user_id)
    if not user:
        raise NotFoundError("Invalid user id.")
    db.session.delete(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise DatabaseError("Error writing to database.")


def find_user(username):
    """
    Return user info for username
    :return basic user info if found
    """
    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        return []
    else:
        return user.basic_info()


def set_availability(user_id, availability):
    """
    Set availability.
    :param user_id: user requesting operation
    :param availability: bool
    :return: full user info
    """
    user = db.session.query(User).get(user_id)
    user.available = availability
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise DatabaseError("Error writing to database.")
    return user.full_info()


def update_location(user_id, lat, long):
    """
    Update user location in database
    :param user_id: requesting user
    :param lat: new latitude
    :param long: new longitude
    :return: full user info
    """
    if (lat < location.MIN_LAT or lat > location.MAX_LAT
            or long < location.MIN_LON or long > location.MAX_LON):
        raise LocationError("Invalid coordinates.")
    user = db.session.query(User).filter_by(id=user_id).first()
    user.last_seen_lat, user.last_seen_long = lat, long
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise DatabaseError("Error writing to database.")
    return user.full_info()

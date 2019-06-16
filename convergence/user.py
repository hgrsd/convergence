from flask import g
from sqlalchemy import exc
from . import http_auth, db
from .models import User


def register_user(username, password):
    """
    Register user.
    :return tuple(status message, status code)
    """
    user = User(username=username, available=False)
    user.hash_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return {"error": {"message": "username exists already"}}, 400
    return {"status": "success"}, 200


def delete_user(user_id):
    """
    Delete user.
    :return tuple(status message, status code)
    """
    user = User.query.get(user_id)
    if not user:
        return {"error": {"message": "invalid user id"}}, 400
    db.session.delete(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"error": {"message": "error writing to database"}}, 400
    return {"status": "success"}, 200


def set_availability(user_id, availability):
    """
    Set availability.
    :param user_id: user requesting operation
    :param availability: bool
    :return: tuple(status message, status code)
    """
    user = User.query.get(user_id)
    user.available = availability
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"error": {"message": "error updating database"}}, 400
    return {"status": "success"}, 200


@http_auth.verify_password
def verify_password(username, password):
    """
    Verify authentication details and set g.user_id
    :param username: string
    :param password: string
    :return: bool
    """
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user_id = user.id
    return True

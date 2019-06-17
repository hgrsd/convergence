from flask import g
from sqlalchemy import exc
from . import http_auth, db
from .models import User


def register_user(username, password):
    """
    Register user.
    :return dict object with body and status code
    """
    user = User(username=username, available=False)
    user.hash_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return {"body": {"error": {"message": "username exists already"}}, "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def delete_user(user_id):
    """
    Delete user.
    :return dict object with body and status code
    """
    user = User.query.get(user_id)
    if not user:
        return {"body": {"error": {"message": "invalid user id"}}, "status_code": 400}
    db.session.delete(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}}, "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def find_user(username):
    """
    Return user info for username
    :return user id
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return {"body": {"error": {"message": "username not found"}}, "status_code": 404}
    else:
        return {"body": {"status": "success", "data": user.basic_info()}, "status_code": 200}


def set_availability(user_id, availability):
    """
    Set availability.
    :param user_id: user requesting operation
    :param availability: bool
    :return: dict object with body and status code
    """
    user = User.query.get(user_id)
    user.available = availability
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error updating database"}}, "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


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

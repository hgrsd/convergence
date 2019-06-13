from flask import jsonify
from .models import User
from . import db


def update_location(user_id, lat, long):
    user = User.query.filter_by(id=user_id).first()
    user.last_seen_lat, user.last_seen_long = lat, long
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": {"message": "error updating location"}}), 400
    return jsonify({"status": "success"})


def get_coordinates(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    else:
        return user.last_seen_lat, user.last_seen_long

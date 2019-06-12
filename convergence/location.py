from flask import Blueprint, request, g, jsonify
from math import cos, sin, atan2, sqrt, radians, degrees
from . import http_auth, db
from .models import *

location = Blueprint("locations", __name__)


@location.route("/loc/update_location", methods=['POST'])
@http_auth.login_required
def update_location():
    x = request.json.get("x")
    y = request.json.get("y")
    user = User.query.filter_by(id=g.user_id).first()
    user.last_x_coord, user.last_y_coord = x, y
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": {"message": "error writing to database"}}), 400
    return jsonify({"status": "success"})


def find_centre_point(locations):
    x_total, y_total, z_total = 0, 0, 0
    for lat, lon in locations:
        lat = radians(float(lat))
        lon = radians(float(lon))
        x_total += cos(lat) * cos(lon)
        y_total += cos(lat) * sin(lon)
        z_total += sin(lat)
    x = float(x_total / len(locations))
    y = float(y_total / len(locations))
    z = float(z_total / len(locations))

    return degrees(atan2(z, sqrt(x * x + y * y))), degrees(atan2(y, x))

from flask import Blueprint, request, g, jsonify
from sqlalchemy import exc
from . import http_auth, db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username')
    pw = request.json.get('password')
    print(username, pw)
    user = User(username=username)
    user.hash_password(pw)
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": {"message": "username exists already"}}), 400
    return "Registered.\n"


@http_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user_id = user.id
    return True

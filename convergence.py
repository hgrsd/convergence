from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
import flask_httpauth

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='postgresql://localhost/convergence',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
auth = flask_httpauth.HTTPBasicAuth()
db = SQLAlchemy(app)
from models import *


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user_id = user.id
    return True


@app.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username')
    pw = request.json.get('password')
    user = User(username=username)
    user.hash_password(pw)
    db.session.add(user)
    db.session.commit()
    return "Registered."


@app.route('/create_group', methods=['POST'])
@auth.login_required
def create_group():
    name = request.json.get('group_name')
    if Group.query.filter_by(name=name).first():
        return False
    group = Group(name=name, owner=g.userid)
    db.session.add(group)
    db.session.commit()
    usergroup = UserGroup(user=g.userid, group=group.id)
    db.session.add(usergroup)
    db.session.commit()
    return "Created.\n"


@app.route('/add_user_to_group', methods=['POST'])
@auth.login_required
def add_user_to_group():
    group = request.json.get('group_id')
    user = request.json.get('user_id')
    if not Group.query.get(group):
        return "Group doesn't exist.\n"
    if not User.query.get(user):
        return "User doesn't exist.\n"
    if not Group.query.get(group).owner == g.user_id:
        return "This isn't your group.\n"
    usergroup = UserGroup(user=user, group=group)
    db.session.add(usergroup)
    db.session.commit()
    return "Added.\n"

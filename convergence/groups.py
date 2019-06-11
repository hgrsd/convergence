from flask import Blueprint, request, g
from . import http_auth, db
from .models import *

groups = Blueprint("groups", __name__)

@groups.route('/create_group', methods=['POST'])
@http_auth.login_required
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


@groups.route('/add_user_to_group', methods=['POST'])
@http_auth.login_required
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

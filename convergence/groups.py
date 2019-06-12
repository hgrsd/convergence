from flask import Blueprint, request, g, jsonify
from . import http_auth, db
from .models import *

groups = Blueprint("groups", __name__)


@groups.route('/groups/create_group', methods=['POST'])
@http_auth.login_required
def create_group():
    name = request.json.get('group_name')
    if Group.query.filter_by(name=name).first():
        return jsonify({"error": {"message": "group name exists already"}}), 400
    group = Group(name=name, owner=g.user_id)
    db.session.add(group)
    db.session.flush()
    usergroup = UserGroup(user_id=g.user_id, group_id=group.id)
    db.session.add(usergroup)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": {"message": "error writing to database"}}), 400
    return jsonify({"status": "success"})


@groups.route('/groups/add_user_to_group', methods=['POST'])
@http_auth.login_required
def add_user_to_group():
    group = request.json.get('group_id')
    user = request.json.get('user_id')
    if not Group.query.get(group):
        return jsonify({"error": {"message": "group does not exist"}}), 400
    if not User.query.get(user):
        return jsonify({"error": {"message": "user does not exist"}}), 400
    if not Group.query.get(group).owner == g.user_id:
        return jsonify({"error": {"message": "permission denied"}}), 400
    usergroup = UserGroup(user_id=user, group_id=group)
    db.session.add(usergroup)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": {"message": "error writing to database"}}), 400
    return jsonify({"status": "success"})

@groups.route('/groups/remove_user_from_group', methods=['POST'])
@http_auth.login_required
def remove_user_from_group():
    group = request.json.get('group_id')
    user = request.json.get('user_id')
    if not Group.query.get(group):
        return jsonify({"error": {"message": "group does not exist"}}), 400
    if not User.query.get(user):
        return jsonify({"error": {"message": "user does not exist"}}), 400
    if not Group.query.get(group).owner == g.user_id:
        return jsonify({"error": {"message": "permission denied"}}), 400
    to_delete = UserGroup.query.filter_by(user_id=user, group_id=group).first()
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": {"message": "error writing to database"}}), 400
    return jsonify({"status": "success"})


@groups.route('/groups/get_members', methods=['GET'])
@http_auth.login_required
def get_members():
    group_id = request.json.get('group_id')
    if not Group.query.get(group_id):
        return jsonify({"error": {"message": "group does not exist"}}), 400
    if not UserGroup.query.filter_by(group_id=group_id, user_id=g.user_id):
        return jsonify({"error": {"message": "access denied"}}), 400
    entries = UserGroup.query.filter_by(group_id=group_id).all()
    return jsonify({"status": "success", "data": list(entry.as_dict() for entry in entries)})


@groups.route('/groups/get_user_groups', methods=['GET'])
@http_auth.login_required
def get_groups():
    my_groups = UserGroup.query.filter_by(user_id=g.user_id)
    if not my_groups:
        return jsonify({"status": "success", "data": {"groups": []}})
    return jsonify({"status": "success", "data": list(group.as_dict() for group in my_groups)})


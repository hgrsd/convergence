from flask import g, jsonify
from .models import *


def create_group(user_id, name):
    if Group.query.filter_by(name=name).first():
        return jsonify({"error": {"message": "group name exists already"}}), 400
    group = Group(name=name, owner=user_id)
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


def add_user_to_group(request_id, user_id, group_id):
    if not Group.query.get(group_id):
        return jsonify({"error": {"message": "group does not exist"}}), 400
    if not User.query.get(user_id):
        return jsonify({"error": {"message": "user does not exist"}}), 400
    if not Group.query.get(group_id).owner == request_id:
        return jsonify({"error": {"message": "permission denied"}}), 400
    usergroup = UserGroup(user_id=user_id, group_id=group_id)
    db.session.add(usergroup)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": {"message": "error writing to database"}}), 400
    return jsonify({"status": "success"})


def remove_user_from_group(request_id, user_id, group_id):
    if not Group.query.get(group_id):
        return jsonify({"error": {"message": "group does not exist"}}), 400
    if not User.query.get(user_id):
        return jsonify({"error": {"message": "user does not exist"}}), 400
    if not Group.query.get(group_id).owner == request_id:
        return jsonify({"error": {"message": "permission denied"}}), 400
    to_delete = UserGroup.query.filter_by(user_id=user_id, group_id=group_id).first()
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": {"message": "error writing to database"}}), 400
    return jsonify({"status": "success"})


def get_members(request_id, group_id):
    if not group_id:
        return jsonify({"error": {"message": "no group_id specified"}}), 400
    if not Group.query.get(group_id):
        return jsonify({"error": {"message": "group does not exist"}}), 400
    if not UserGroup.query.filter_by(user_id=request_id, group_id=group_id):
        return jsonify({"error": {"message": "access denied"}}), 400
    entries = UserGroup.query.filter_by(group_id=group_id).all()
    return list(entry.as_dict() for entry in entries)


def get_groups(user_id):
    my_groups = UserGroup.query.filter_by(user_id=user_id)
    if not my_groups:
        return jsonify({"status": "success", "data": {"groups": []}})
    return jsonify({"status": "success", "data": list(group.as_dict() for group in my_groups)})


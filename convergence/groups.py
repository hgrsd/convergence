from .models import *


def create_group(user_id, name):
    """
    Create new group.
    :param user_id: the user creating the group
    :param name: the name of the new group
    :return: tuple(status message, status code)
    """
    if Group.query.filter_by(name=name).first():
        return {"error": {"message": "group name exists already"}}, 400
    group = Group(name=name, owner=user_id)
    db.session.add(group)
    db.session.flush()
    usergroup = UserGroup(user_id=user_id, group_id=group.id)
    db.session.add(usergroup)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"error": {"message": "error writing to database"}}, 400
    return {"status": "success"}, 200


def delete_group(user_id, group_id):
    """
    Delete a group.
    :param user_id: user deleting the group (must be group owner)
    :param group_id: group to be deleted
    :return: tuple(status message, status code)
    """
    to_delete = Group.query.get(group_id)
    if not to_delete:
        return {"error": {"message": "group does not exist"}}, 400
    if not to_delete.owner == user_id:
        return {"error": {"message": "permission denied"}}, 400
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"error": {"message": "error writing to database"}}, 400
    return {"status": "success"}, 200


def add_user_to_group(request_id, user_id, group_id):
    """
    Add user to a group.
    :param request_id: user requesting operation (must be group owner)
    :param user_id: user to be added to group
    :param group_id: group to add user to
    :return: tuple(status message, status code)
    """
    if not Group.query.get(group_id):
        return {"error": {"message": "group does not exist"}}, 400
    if not User.query.get(user_id):
        return {"error": {"message": "user does not exist"}}, 400
    if not Group.query.get(group_id).owner == request_id:
        return {"error": {"message": "permission denied"}}, 400
    usergroup = UserGroup(user_id=user_id, group_id=group_id)
    db.session.add(usergroup)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"error": {"message": "error writing to database"}}, 400
    return {"status": "success"}, 200


def remove_user_from_group(request_id, user_id, group_id):
    """
    Delete user from a group.
    :param request_id: user requesting operation (must be group owner)
    :param user_id: user to be deleted from group
    :param group_id: group to delete user from
    :return: tuple(status message, status code)
    """
    if not Group.query.get(group_id):
        return {"error": {"message": "group does not exist"}}, 400
    if not User.query.get(user_id):
        return {"error": {"message": "user does not exist"}}, 400
    if not Group.query.get(group_id).owner == request_id:
        return {"error": {"message": "permission denied"}}, 400
    to_delete = UserGroup.query.filter_by(user_id=user_id, group_id=group_id).first()
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"error": {"message": "error writing to database"}}, 400
    return {"status": "success"}, 200


def get_members(request_id, group_id):
    """
    Get members from group
    :param request_id: user requesting operation (must be group member)
    :param group_id: group of which members are requested
    :return: tuple(object with member information / status message, status code)
    """
    if not group_id:
        return {"error": {"message": "no group_id specified"}}, 400
    if not Group.query.get(group_id):
        return {"error": {"message": "group does not exist"}}, 400
    if not UserGroup.query.filter_by(user_id=request_id, group_id=group_id):
        return {"error": {"message": "access denied"}}, 400
    entries = UserGroup.query.filter_by(group_id=group_id).all()
    if not entries:
        return {"status": "success", "data": []}, 200
    users = [User.query.get(entry.user_id) for entry in entries]
    return {"status": "success", "data": [user.as_dict() for user in users]}, 200


def get_available_members(request_id, group_id):
    """
    Get available members from group
    :param request_id: user requesting operation (must be group member)
    :param group_id: group of which members are requested
    :return: tuple(object with member information / status message, status code)
    """
    if not group_id:
        return {"error": {"message": "no group_id specified"}}, 400
    if not Group.query.get(group_id):
        return {"error": {"message": "group does not exist"}}, 400
    if not UserGroup.query.filter_by(user_id=request_id, group_id=group_id):
        return {"error": {"message": "access denied"}}, 400
    entries = UserGroup.query.filter_by(group_id=group_id).all()
    available_users = []
    for entry in entries:
        user = User.query.filter_by(id=entry.user_id, available=True).first()
        if user:
            available_users.append(user)
    if not available_users:
        return {"status": "success", "data": []}, 200
    return {"status": "success", "data": [user.as_dict() for user in available_users]}, 200


def get_groups(user_id):
    """
    Get groups of which user is a member.
    :param user_id: user requesting operation
    :return: tuple(group information / status message, status code)
    """
    my_groups = UserGroup.query.filter_by(user_id=user_id)
    if not my_groups:
        return {"status": "success", "data": {"groups": []}}, 200
    return {"status": "success", "data": list(group.as_dict() for group in my_groups)}, 200

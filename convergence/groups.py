from . import db
from .models import Group, UserGroup, User
from sqlalchemy import exc


def create_group(user_id, name):
    """
    Create new group.
    :param user_id: the user creating the group
    :param name: the name of the new group
    :return: dict object with body and status code
    """
    group = Group(name=name, owner=user_id)
    db.session.add(group)
    try: 
        db.session.flush()
    except exc.IntegrityError:
        return {"body": {"error": {"message": "you already own a group with that name"}}, "status_code": 400}
    usergroup = UserGroup(user_id=user_id, group_id=group.id)
    db.session.add(usergroup)
    try:
        db.session.commit()
    except: 
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}}, "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def delete_group(user_id, group_id):
    """
    Delete a group.
    :param user_id: user deleting the group (must be group owner)
    :param group_id: group to be deleted
    :return: dict object with body and status code
    """
    to_delete = Group.query.get(group_id)
    if not to_delete:
        return {"body": {"error": {"message": "group does not exist"}}, "status_code": 400}
    if not to_delete.owner == user_id:
        return {"body": {"error": {"message": "permission denied"}}, "status_code": 400}
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}}, "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def add_user_to_group(request_id, user_id, group_id):
    """
    Add user to a group.
    :param request_id: user requesting operation (must be group owner)
    :param user_id: user to be added to group
    :param group_id: group to add user to
    :return: dict object with body and status code
    """
    if not Group.query.get(group_id):
        return {"body": {"error": {"message": "group does not exist"}}, "status_code": 400}
    if not User.query.get(user_id):
        return {"body": {"error": {"message": "user does not exist"}}, "status_code": 400}
    if not Group.query.get(group_id).owner == request_id:
        return {"body": {"error": {"message": "permission denied"}}, "status_code": 400}
    usergroup = UserGroup(user_id=user_id, group_id=group_id)
    db.session.add(usergroup)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}}, "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def remove_user_from_group(request_id, user_id, group_id):
    """
    Delete user from a group.
    :param request_id: user requesting operation (must be group owner)
    :param user_id: user to be deleted from group
    :param group_id: group to delete user from
    :return: dict object with body and status code
    """
    to_delete = UserGroup.query.filter_by(user_id=user_id, group_id=group_id).first()
    if not to_delete:
        return {"body": {"error": {"message": "invalid group or member"}}, "status_code": 400}
    if not Group.query.get(group_id).owner == request_id:
        return {"body": {"error": {"message": "permission denied"}}, "status_code": 400}
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}}, "status_code": 400}
    return {"status": "success"}, 200


def get_members(request_id, group_id):
    """
    Get members from group
    :param request_id: user requesting operation (must be group member)
    :param group_id: group of which members are requested
    :return: dict object with body and status code
    """
    if not UserGroup.query.filter_by(user_id=request_id, group_id=group_id):
        return {"body": {"error": {"message": "access denied"}}, "status_code": 400}
    users = db.session.query(User).join(UserGroup, User.id == UserGroup.user_id) \
            .filter(UserGroup.group_id == group_id) \
            .all()
    if not users:
        return {"body": {"status": "success", "data": []}, "status_code": 200}
    return {"body": {"status": "success", "data": [user.basic_info() for user in users]}, "status_code": 200}


def get_owned_groups(user_id):
    """
    Get groups owned by user_id
    :param user_id: user requesting operation
    :return list of groups (as dict) owned by user_id
    """
    groups_owned = Group.query.filter_by(owner=user_id).all()
    if not groups_owned:
        return {"body": {"status": "success", "data": []}, "status_code": 200}
    else:
        return {"body": {"status": "success", "data": [group.as_dict() for group in groups_owned]}, "status_code": 200}


def get_available_members(request_id, group_id):
    """
    Get available members from group
    :param request_id: user requesting operation (must be group member)
    :param group_id: group of which members are requested
    :return: dict object with body and status code
    """
    if not UserGroup.query.filter_by(user_id=request_id, group_id=group_id):
        return {"body": {"error": {"message": "access denied"}}, "status_code": 400}
    users = db.session.query(User).join(UserGroup, User.id == UserGroup.user_id) \
            .filter(UserGroup.group_id == group_id, User.available == True) \
            .all()
    if not users:
        return {"body": {"status": "success", "data": []}, "status_code": 200}
    return {"body": {"status": "success", "data": [user.basic_info() for user in users]}, "status_code": 200}


def get_groups(user_id):
    """
    Get groups of which user is a member.
    :param user_id: user requesting operation
    :return: dict object with body and status code
    """
    groups = db.session.query(Group).join(UserGroup, Group.id == UserGroup.group_id) \
            .filter(UserGroup.user_id == user_id) \
            .all()
    if not groups:
        return {"body": {"status": "success", "data": {"groups": []}}, "status_code": 200}
    return {"body": {"status": "success", "data": [group.as_dict() for group in groups]}, "status_code": 200}

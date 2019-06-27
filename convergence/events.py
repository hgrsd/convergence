from . import db
from .models import Event, UserEvent, User
from sqlalchemy import exc


def create_event(user_id, name):
    """
    Create new event.
    :param user_id: the user creating the event
    :param name: the name of the new event
    :return: dict object with body and status code
    """
    event = Event(name=name, owner=user_id)
    db.session.add(event)
    try:
        db.session.flush()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}},
                "status_code": 400}
    userevent = UserEvent(user_id=user_id, event_id=event.id)
    db.session.add(userevent)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}},
                "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def delete_event(user_id, event_id):
    """
    Delete a event.
    :param user_id: user deleting the event (must be event owner)
    :param event_id: event to be deleted
    :return: dict object with body and status code
    """
    to_delete = Event.query.get(event_id)
    if not to_delete:
        return {"body": {"error": {"message": "event does not exist"}},
                "status_code": 400}
    if not to_delete.owner == user_id:
        return {"body": {"error": {"message": "permission denied"}},
                "status_code": 400}
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}},
                "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def add_user_to_event(request_id, user_id, event_id):
    """
    Add user to a event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be added to event
    :param event_id: event to add user to
    :return: dict object with body and status code
    """
    if not Event.query.get(event_id):
        return {"body": {"error": {"message": "event does not exist"}},
                "status_code": 400}
    if not User.query.get(user_id):
        return {"body": {"error": {"message": "user does not exist"}},
                "status_code": 400}
    if not Event.query.get(event_id).owner == request_id:
        return {"body": {"error": {"message": "permission denied"}},
                "status_code": 400}
    userevent = UserEvent(user_id=user_id, event_id=event_id)
    db.session.add(userevent)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}},
                "status_code": 400}
    return {"body": {"status": "success"}, "status_code": 200}


def remove_user_from_event(request_id, user_id, event_id):
    """
    Delete user from a event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be deleted from event
    :param event_id: event to delete user from
    :return: dict object with body and status code
    """
    to_delete = UserEvent.query.filter_by(user_id=user_id, event_id=event_id) \
                               .first()
    if not to_delete:
        return {"body": {"error": {"message": "invalid event or member"}},
                "status_code": 400}
    if not Event.query.get(event_id).owner == request_id:
        return {"body": {"error": {"message": "permission denied"}},
                "status_code": 400}
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"body": {"error": {"message": "error writing to database"}},
                "status_code": 400}
    return {"status": "success"}, 200


def get_members(request_id, event_id):
    """
    Get members from event
    :param request_id: user requesting operation (must be event member)
    :param event_id: event of which members are requested
    :return: dict object with body and status code
    """
    if not UserEvent.query.filter_by(user_id=request_id, event_id=event_id).first():
        return {"body": {"error": {"message": "access denied"}},
                "status_code": 400}
    users = db.session.query(User) \
                      .join(UserEvent, User.id == UserEvent.user_id) \
                      .filter(UserEvent.event_id == event_id) \
                      .all()
    if not users:
        return {"body": {"status": "success", "data": []},
                "status_code": 200}
    return {"body": {"status": "success",
            "data": [user.basic_info() for user in users]},
            "status_code": 200}


def get_owned_events(user_id):
    """
    Get events owned by user_id
    :param user_id: user requesting operation
    :return list of events (as dict) owned by user_id
    """
    events_owned = Event.query.filter_by(owner=user_id).all()
    if not events_owned:
        return {"body": {"status": "success", "data": []}, "status_code": 200}
    else:
        return {"body": {"status": "success",
                "data": [event.as_dict() for event in events_owned]},
                "status_code": 200}


def get_available_members(request_id, event_id):
    """
    Get available members from event
    :param request_id: user requesting operation (must be event member)
    :param event_id: event of which members are requested
    :return: dict object with body and status code
    """
    if not UserEvent.query.filter_by(user_id=request_id, event_id=event_id).first():
        return {"body": {"error": {"message": "access denied"}},
                "status_code": 400}
    users = db.session.query(User) \
                      .join(UserEvent, User.id == UserEvent.user_id) \
                      .filter(UserEvent.event_id == event_id,
                              User.available == True) \
                      .all()
    if not users:
        return {"body": {"status": "success", "data": []},
                "status_code": 200}
    return {"body": {"status": "success",
            "data": [user.basic_info() for user in users]},
            "status_code": 200}


def get_events(user_id):
    """
    Get events of which user is a member.
    :param user_id: user requesting operation
    :return: dict object with body and status code
    """
    events = db.session.query(Event) \
                       .join(UserEvent, Event.id == UserEvent.event_id) \
                       .filter(UserEvent.user_id == user_id) \
                       .all()
    if not events:
        return {"body": {"status": "success", "data": {"events": []}},
                "status_code": 200}
    return {"body": {"status": "success",
            "data": [event.as_dict() for event in events]},
            "status_code": 200}

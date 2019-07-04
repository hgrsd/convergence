import datetime
from sqlalchemy.exc import SQLAlchemyError

from . import db
from . import exceptions
from .models import Event, UserEvent, User


def create_event(user_id, name):
    """
    Create new event.
    :param user_id: the user creating the event
    :param name: the name of the new event
    :return: event info as dict
    """
    event = Event(event_name=name, event_owner_id=user_id,
                  creation_date=datetime.datetime.utcnow())
    db.session.add(event)
    try:
        db.session.flush()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {e.message}")
    userevent = UserEvent(user_id=user_id, event_id=event.id)
    db.session.add(userevent)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {e.message}")
    return event.as_dict()


def delete_event(user_id, event_id):
    """
    Delete a event.
    :param user_id: user deleting the event (must be event owner)
    :param event_id: event to be deleted
    """
    to_delete = db.session.query(Event).get(event_id)
    if not to_delete:
        raise exceptions.NotFoundError("Invalid event id.")
    if not to_delete.owner == user_id:
        raise exceptions.PermissionError("Permission denied.")
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {e.message}")
    return None


def add_user_to_event(user_id, event_id):
    """
    Add user to a event. Make sure event ownership checks are done BEFORE this
    function is called.
    :param user_id: user to be added to event
    :param event_id: event to add user to
    """
    event = db.session.query(Event).get(event_id)
    if not event:
        raise exceptions.NotFoundError("Invalid event id.")
    if not db.session.query(User).get(user_id):
        raise exceptions.NotFoundError("Invalid user id.")
    userevent = UserEvent(user_id=user_id, event_id=event_id)
    db.session.add(userevent)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {e.message}")
    return None


def leave_event(request_id, event_id):
    """
    Leave an event.
    :param request_id: user requesting operation (must be event member)
    :param event_id: event to leave
    """
    to_delete = db.session.query(UserEvent).filter_by(user_id=request_id,
                                                      event_id=event_id) \
                                           .first()
    if not to_delete:
        raise exceptions.NotFoundError("Invalid group, or user not a member.")
    if db.session.query(Event).get(event_id).event_owner_id == request_id:
        raise exceptions.InvalidRequestError("Cannot leave owned event.")
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {e.message}")
    return None


def remove_user_from_event(request_id, user_id, event_id):
    """
    Delete user from a event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be deleted from event
    :param event_id: event to delete user from
    """
    to_delete = db.session.query(UserEvent).filter_by(user_id=user_id,
                                                      event_id=event_id) \
                                           .first()
    if not to_delete:
        raise exceptions.NotFoundError("Invalid group id or user id.")
    if not db.session.query(Event).get(event_id).event_owner_id == request_id:
        raise exceptions.PermissionError("Permission denied.")
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {e.message}")
    return None


def get_members(request_id, event_id):
    """
    Get members from event
    :param request_id: user requesting operation (must be event member)
    :param event_id: event of which members are requested
    :return: basic user info for all users in group
    """
    if not db.session.query(UserEvent).filter_by(user_id=request_id,
                                                 event_id=event_id) \
                                      .first():
        raise exceptions.PermissionError("Permission denied.")
    users = db.session.query(User) \
                      .join(UserEvent, User.userevents) \
                      .filter(UserEvent.event_id == event_id) \
                      .all()
    if not users:
        return []
    return [user.basic_info() for user in users]


def get_owned_events(user_id):
    """
    Get events owned by user_id
    :param user_id: user requesting operation
    :return list of events which user owns
    """
    events_owned = db.session.query(Event) \
                             .filter_by(event_owner_id=user_id).all()
    if not events_owned:
        return []
    return [event.as_dict() for event in events_owned]


def get_events(user_id):
    """
    Get events of which user is a member.
    :param user_id: user requesting operation
    :return: list of events of which user is a member
    """
    query_result = db.session.query(User, Event) \
                             .join(Event) \
                             .join(UserEvent) \
                             .filter(UserEvent.user_id == user_id) \
                             .all()
    if not query_result:
        return []
    events = []
    for i, entry in enumerate(query_result):
        events.append(entry[1].as_dict())
        events[i]["owner_name"] = entry[0].username
    return events

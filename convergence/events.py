import datetime

from sqlalchemy.exc import IntegrityError

from . import db
from .models import Event, UserEvent, User
from .exceptions import DatabaseError, PermissionError, NotFoundError


def create_event(user_id, name):
    """
    Create new event.
    :param user_id: the user creating the event
    :param name: the name of the new event
    :return: event info as dict
    """
    event = Event(name=name, owner=user_id,
                  creation_date=datetime.datetime.utcnow())
    db.session.add(event)
    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        raise DatabaseError("Error writing to database.")
    userevent = UserEvent(user_id=user_id, event_id=event.id)
    db.session.add(userevent)
    try:
        db.session.commit()
    except IntegrityError as e:
        print(e._message)
        db.session.rollback()
        raise DatabaseError("Error writing to database.")
    return event.as_dict()


def delete_event(user_id, event_id):
    """
    Delete a event.
    :param user_id: user deleting the event (must be event owner)
    :param event_id: event to be deleted
    """
    to_delete = db.session.query(Event).get(event_id)
    if not to_delete:
        raise NotFoundError("Invalid event id.")
    if not to_delete.owner == user_id:
        raise PermissionError("Permission denied. Must be event owner.")
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise DatabaseError("Error writing to database.")


def add_user_to_event(request_id, user_id, event_id):
    """
    Add user to a event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be added to event
    :param event_id: event to add user to
    """
    event = db.session.query(Event).get(event_id)
    if not event:
        raise NotFoundError("Invalid event id.")
    if not db.session.query(User).get(user_id):
        raise NotFoundError("Invalid user id.")
    if not event.owner == request_id:
        raise PermissionError("Permission denied. Must be event owner.")
    userevent = UserEvent(user_id=user_id, event_id=event_id)
    db.session.add(userevent)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise DatabaseError("Error writing to database.")


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
        raise NotFoundError("Invalid group id or user id.")
    if not db.session.query(Event).get(event_id).owner == request_id:
        raise PermissionError("Permission denied. Must be event owner.")
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise DatabaseError("Error writing to database.")


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
        raise PermissionError("Permission denied. Must be event member.")
    users = db.session.query(User) \
                      .join(UserEvent, User.id == UserEvent.user_id) \
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
    events_owned = db.session.query(Event).filter_by(owner=user_id).all()
    if not events_owned:
        return []
    else:
        return [event.as_dict() for event in events_owned]


def get_events(user_id):
    """
    Get events of which user is a member.
    :param user_id: user requesting operation
    :return: list of events of which user is a member
    """
    events = db.session.query(Event) \
                       .join(UserEvent, Event.id == UserEvent.event_id) \
                       .filter(UserEvent.user_id == user_id) \
                       .all()
    if not events:
        return []
    return [event.as_dict() for event in events]

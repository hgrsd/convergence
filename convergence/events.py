import datetime

from . import exceptions
from .repositories import EventStore, UserStore, UserEventStore
from .models import Event, UserEvent

event_store = EventStore()
user_store = UserStore()
userevent_store = UserEventStore()


def create_event(user_id, name):
    """
    Create new event.
    :param user_id: the user creating the event
    :param name: the name of the new event
    :return: event info as dict
    """
    event = Event(event_name=name, event_owner_id=user_id,
                  creation_date=datetime.datetime.utcnow())
    event_store.add_event(event)
    userevent = UserEvent(user_id=user_id, event_id=event.id)
    userevent_store.add_userevent(userevent)
    return event.as_dict()


def delete_event(user_id, event_id):
    """
    Delete a event.
    :param user_id: user deleting the event (must be event owner)
    :param event_id: event to be deleted
    """
    to_delete = event_store.get_event_by_id(event_id)
    if not to_delete:
        raise exceptions.NotFoundError("Invalid event id.")
    if not to_delete.owner == user_id:
        raise exceptions.PermissionError("Permission denied.")
    event_store.delete_event(to_delete)
    return None


def add_user_to_event(user_id, event_id):
    """
    Add user to a event. Make sure event ownership checks are done BEFORE this
    function is called.
    :param user_id: user to be added to event
    :param event_id: event to add user to
    """
    event = event_store.get_event_by_id(event_id)
    if not event:
        raise exceptions.NotFoundError("Invalid event id.")
    if not user_store.get_user_by_id(user_id):
        raise exceptions.NotFoundError("Invalid user id.")
    userevent = UserEvent(user_id=user_id, event_id=event_id)
    userevent_store.add_userevent(userevent)
    return None


def leave_event(request_id, event_id):
    """
    Leave an event.
    :param request_id: user requesting operation (must be event member)
    :param event_id: event to leave
    """
    to_delete = userevent_store.get_userevent(request_id, event_id)
    if not to_delete:
        raise exceptions.NotFoundError("Invalid group or user not a member.")
    if request_id == event_store.get_owner_id(event_id):
        raise exceptions.InvalidRequestError("Cannot leave owned event.")
    userevent_store.delete_userevent(to_delete)
    return None


def remove_user_from_event(request_id, user_id, event_id):
    """
    Delete user from a event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be deleted from event
    :param event_id: event to delete user from
    """
    to_delete = userevent_store.get_userevent(user_id, event_id)
    if not to_delete:
        raise exceptions.NotFoundError("Invalid group id or user id.")
    if request_id != event_store.get_owner_id(event_id):
        raise exceptions.PermissionError("Permission denied.")
    userevent_store.delete_userevent(to_delete)
    return None


def get_members(request_id, event_id):
    """
    Get members from event
    :param request_id: user requesting operation (must be event member)
    :param event_id: event of which members are requested
    :return: basic user info for all users in group
    """
    if not userevent_store.get_userevent(request_id, event_id):
        raise exceptions.PermissionError("Permission denied.")
    users = userevent_store.get_users_by_event(event_id)
    if not users:
        return []
    return [user.basic_info() for user in users]


def get_owned_events(user_id):
    """
    Get events owned by user_id
    :param user_id: user requesting operation
    :return list of events which user owns
    """
    events_owned = event_store.get_events_by_owner(user_id)
    if not events_owned:
        return []
    return [event.as_dict() for event in events_owned]


def get_events(user_id):
    """
    Get events of which user is a member.
    :param user_id: user requesting operation
    :return: list of events of which user is a member,
             including name of event owner
    """
    user_events = userevent_store.get_events_by_user(user_id)
    if not user_events:
        return []
    events = []
    for user, event in user_events:  # user = event owner
        event = event.as_dict()
        event["owner_name"] = user.screen_name
        events.append(event)
    return events

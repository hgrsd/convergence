import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from . import db
from . import events
from . import exceptions
from .models import Event, User, UserInvite


def invite_user_to_event(request_id, user_id, event_id):
    """
    Invite user to an event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be invited to event
    :param event_id: event to add user to
    """
    event = db.session.query(Event).get(event_id)
    if not event:
        raise exceptions.NotFoundError("Invalid event id.")
    if not db.session.query(User).get(user_id):
        raise exceptions.NotFoundError("Invalid user id.")
    if not event.event_owner_id == request_id:
        raise exceptions.PermissionError("Permission denied.")
    userinvite = UserInvite(inviter_id=request_id, invitee_id=user_id,
                            event_id=event_id)
    db.session.add(userinvite)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {str(e)}")
    return None


def get_invitations(user_id):
    """
    Get all pending invitations for user
    :param user_id: id of requesting user
    :return: list of pending invitations with user and event info
    """
    event_owner = sa.alias(User)
    inviter = sa.alias(User)
    query_result = db.session.query(Event,
                                    event_owner.c.username,
                                    UserInvite.id,
                                    inviter.c.username) \
                             .join(UserInvite, Event.userinvites) \
                             .join(event_owner, Event.event_owners) \
                             .join(inviter, UserInvite.inviter_ids) \
                             .filter(UserInvite.invitee_id == user_id) \
                             .all()
    if not query_result:
        return []
    invitations = []
    for i, entry in enumerate(query_result):
        invitations.append(entry[0].as_dict())
        invitations[i]["owner_name"] = entry[1]
        invitations[i]["invitation_id"] = entry[2]
        invitations[i]["inviter_name"] = entry[3]
    return invitations


def respond_to_invitation(request_id, invite_id, accept):
    """
    Respond to event invitation
    :param request_id: id of user responding to invite
    :param invite_id: id of the UserInvite
    :param accept: bool, True = accept, False = Reject
    :return None if accept is False, Event info if accept is True
    """
    userinvite = db.session.query(UserInvite).get(invite_id)
    if not userinvite:
        raise exceptions.NotFoundError("Invite not found.")
    if not userinvite.invitee_id == request_id:
        raise exceptions.PermissionError("Permission denied.")
    if accept is True:
        user_id = userinvite.invitee_id
        event_id = userinvite.event_id
        events.add_user_to_event(user_id, event_id)
    db.session.delete(userinvite)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise exceptions.DatabaseError(f"Error: {str(e)}")
    return db.session.query(Event).get(event_id).as_dict() if accept else None

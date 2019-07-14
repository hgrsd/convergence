from convergence import events
from convergence import exceptions
from convergence.models import UserInvite
from convergence.repo import UserInviteStore, EventStore, UserStore

userinvite_store = UserInviteStore()
event_store = EventStore()
user_store = UserStore()


def invite_user_to_event(request_id, user_id, event_id):
    """
    Invite user to an event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be invited to event
    :param event_id: event to add user to
    """
    event = event_store.get_event_by_id(event_id)
    if not event or not event.event_owner_id == request_id:
        raise exceptions.NotFoundError("Invalid event id.")
    if not user_store.get_user_by_id(user_id):
        raise exceptions.NotFoundError("Invalid user id.")
    userinvite = UserInvite(inviter_id=request_id, invitee_id=user_id,
                            event_id=event_id)
    userinvite_store.add_userinvite(userinvite)
    return userinvite.as_dict()


def get_invitations(user_id):
    """
    Get all pending invitations for user
    :param user_id: id of requesting user
    :return: list of pending invitations with user and event info
    """
    invitations_data = userinvite_store.get_invitations_by_user(user_id)
    if not invitations_data:
        return []
    invitations = []
    for i, entry in enumerate(invitations_data):
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
    :return: None if accept is False, Event info if accept is True
    """
    userinvite = userinvite_store.get_invitation_by_id(invite_id)
    if not userinvite or not userinvite.invitee_id == request_id:
        raise exceptions.NotFoundError("Invite not found.")
    if accept:
        user_id = userinvite.invitee_id
        event_id = userinvite.event_id
        events.add_user_to_event(user_id, event_id)
    userinvite_store.delete_userinvite(invite_id)
    return event_store.get_event_by_id(event_id).as_dict() if accept else None

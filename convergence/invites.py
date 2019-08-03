from convergence import events
from convergence import exceptions
from convergence.models import UserInvite
from convergence.repo import UserInviteStore, EventStore, UserStore, \
                             UserEventStore

MAX_INVITES_PER_REQUEST = 100

userinvite_store = UserInviteStore()
userevent_store = UserEventStore()
event_store = EventStore()
user_store = UserStore()


def invite_user_to_event(request_id, user_id, event_id):
    """
    Invite user to an event.
    :param request_id: user requesting operation (must be event owner)
    :param user_id: user to be invited to event
    :param event_id: event to add user to
    """
    if request_id == user_id:
        raise exceptions.InvalidRequestError("Cannot invite yourself.")
    event = event_store.get_event_by_id(event_id)
    if not event or not event.event_owner_id == request_id:
        raise exceptions.NotFoundError("Invalid event id.")
    if not user_store.get_user_by_id(user_id):
        raise exceptions.NotFoundError("Invalid user id.")
    if userevent_store.get_userevent(user_id, event_id):
        raise exceptions.InvalidRequestError("User already a member of event.")
    if userinvite_store.get_invite_by_details(user_id, event_id):
        raise exceptions.InvalidRequestError("Invite already pending.")
    userinvite = UserInvite(
        inviter_id=request_id,
        invitee_id=user_id,
        event_id=event_id
    )
    userinvite_store.add_userinvite(userinvite)
    return userinvite.as_dict()


def invite_users_to_event(request_id, emails, event_id):
    """
    Invite multiple users to an event given their usernames.
    :param request_id: user requesting operation (must be event owner)
    :param emails: emails of users to be invited to the event
    :param event_id: event to add user to
    :return: usernames, which weren't invited successfully
    """
    if len(emails) > MAX_INVITES_PER_REQUEST:
        raise exceptions.InvalidRequestError("Too many invites per request.")

    event = event_store.get_event_by_id(event_id)
    if not event or not event.event_owner_id == request_id:
        raise exceptions.NotFoundError("Invalid event id.")

    userinvites = userinvite_store.get_users_by_event(event_id)
    already_pending = set(u.id for u in userinvites) if userinvites else {}
    userevents = userevent_store.get_users_by_event(event_id)
    already_accepted = set(u.id for u in userevents) if userevents else {}

    # TODO: figure out what to do with already rejected

    users_to_process = set(emails)

    # TODO: also allow to bulk invite by phone numbers and user IDs
    users = user_store.get_users_by_emails(emails)
    userinvites = []

    for user in users:
        if (user.id == request_id or
                user.id in already_pending or
                user.id in already_accepted):
            continue
        userinvites.append(UserInvite(
            inviter_id=request_id,
            invitee_id=user.id,
            event_id=event_id
        ))
        users_to_process.remove(user.email)

    userinvite_store.add_userinvites(userinvites)

    return users_to_process


def get_invites(user_id):
    """
    Get all pending invites for user
    :param user_id: id of requesting user
    :return: list of pending invites with user and event info
    """
    invites_data = userinvite_store.get_invites_by_user(user_id)
    if not invites_data:
        return []
    invites = []
    for i, entry in enumerate(invites_data):
        invites.append(entry[0].as_dict())
        invites[i]["owner_name"] = entry[1]
        invites[i]["invite_id"] = entry[2]
        invites[i]["inviter_name"] = entry[3]
    return invites


def respond_to_invite(request_id, invite_id, accept):
    """
    Respond to event invite
    :param request_id: id of user responding to invite
    :param invite_id: id of the UserInvite
    :param accept: bool, True = accept, False = Reject
    :return: None if accept is False, Event info if accept is True
    """
    userinvite = userinvite_store.get_invite_by_id(invite_id)
    if not userinvite or not userinvite.invitee_id == request_id:
        raise exceptions.NotFoundError("Invite not found.")
    if accept:
        print("Hoi")
        userevent = events.add_user_to_event_from_invite(userinvite)
        return userevent
    else:
        userinvite_store.delete_userinvite(userinvite)
        return None

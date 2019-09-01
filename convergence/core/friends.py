from convergence.utils import exceptions
from convergence.data.models import FriendInvite
from convergence.data.repo import UserStore, FriendStore

MAX_INVITES_PER_REQUEST = 100

user_store = UserStore()
friend_store = FriendStore()


def get_friendships(request_id):
    """
    Get list of friends for user
    :param request_id: requesting user
    :return: List of Friendships (screen name added)
    """
    friends = friend_store.get_friendships_by_user(request_id)
    if friends:
        return_list = []
        for i, friend in enumerate(friends):
            return_list.append(friend[0].as_dict())
            return_list[0]["friend_name"] = friend[1]
        return return_list
    return []


def propose_friendship(request_id, user_id):
    """
    Propose friendship to a user
    :param request_id: user requesting operation
    :param user_id: user to befriend
    :return FriendInvite
    """
    if request_id == user_id:
        raise exceptions.InvalidRequestError("Cannot befriend yourself.")
    to_befriend = user_store.get_user_by_id(user_id)
    if not to_befriend:
        raise exceptions.NotFoundError("Invalid user id.")
    if friend_store.get_invite_by_details(request_id, user_id):
        raise exceptions.InvalidRequestError("Invite already pending.")
    friendinvite = FriendInvite(
        requesting_id=request_id,
        requested_id=user_id
    )
    friend_store.add_friendinvite(friendinvite)
    return friendinvite.as_dict()


def propose_friendships(request_id, emails):
    """
    Invite multiple users as friends given their usernames.
    :param request_id: user requesting operation
    :param emails: emails of users to befriend
    :return: usernames which weren't invited successfully
    """
    if len(emails) > MAX_INVITES_PER_REQUEST:
        raise exceptions.InvalidRequestError("Too many invites per request.")

    inv = friend_store.get_pending_invites_sent(request_id)
    already_pending = set(u.requested_id for u in inv) if inv else {}
    friends = friend_store.get_friendships_by_user(request_id)
    already_accepted = set(u.friend_b_id for u in friends) if friends else {}

    # TODO: figure out what to do with already rejected

    users_to_process = set(emails)

    # TODO: also allow to bulk invite by phone numbers and user IDs
    users = user_store.get_users_by_emails(emails)
    friendinvites = []

    for user in users:
        if (user.id == request_id or
                user.id in already_pending or
                user.id in already_accepted):
            continue
        friendinvites.append(FriendInvite(
            requesting_id=request_id,
            requested_id=user.id,
        ))
        users_to_process.remove(user.email)

    friend_store.add_friendinvites(friendinvites)

    return users_to_process


def get_invites(request_id):
    """
    Get all pending invites for user
    :param request_id: id of requesting user
    :return: list of pending invites with user and event info
    """
    invites_data = friend_store.get_pending_invites_received(request_id)
    if not invites_data:
        return []
    invites = []
    for i, entry in enumerate(invites_data):
        invites.append(entry[0].as_dict())
        invites[i].update(entry[1].basic_info())
    return invites


def respond_to_invite(request_id, invite_id, accept):
    """
    Respond to friend invite
    :param request_id: id of user responding to invite
    :param invite_id: id of the FriendInvite
    :param accept: bool, True = accept, False = Reject
    :return: None if accept is False, Friend info if accept is True
    """
    friendships = []
    friendinvite = friend_store.get_invite_by_id(invite_id)
    if not friendinvite or not friendinvite.requested_id == request_id:
        raise exceptions.NotFoundError("Invite not found.")
    if accept:
        friendships = [
            friend.as_dict() for friend in
            friend_store.add_friendship_from_invite(friendinvite)
        ]
    else:
        friend_store.delete_friendinvite(friendinvite)
    return friendships


def delete_friendship(friend_a, friend_b):
    """
    Delete friendship
    :param friend_a: id of friend a
    :param friend_b: id of friend b
    """
    friend_store.delete_friendship(friend_a, friend_b)

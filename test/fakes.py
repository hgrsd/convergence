import datetime
from convergence.models import Event, User, UserInvite, UserEvent, \
                               Friend, FriendInvite


def get_fake_friendships():
    a = Friend(
        friend_a_id=3,
        friend_b_id=7,
        creation_date=datetime.utcnow()
    )
    b = Friend(
        friend_a_id=4,
        friend_b_id=8,
        creation_date=datetime.utcnow()
    )
    return [a, b]


def get_fake_friendinvite(requesting_id, requested_id):
    return FriendInvite(
        requesting_id=requesting_id,
        requested_id=requested_id
    )


def get_fake_friendinvite_by_id(id):
    return FriendInvite(
        id=id,
        requesting_id=3,
        requested_id=8
    )


def get_fake_friendinvites_by_user(user_id):
    return [FriendInvite(
        requesting_id=user_id,
        requested_id=5
    )]


def get_fake_pending_invites_by_user(user_id):
    return [(
        FriendInvite(
            requesting_id=5,
            requested_id=user_id
         ),
        get_fake_user_by_id(8)
    )]


def get_fake_friendship(friend_a, friend_b):
    return Friend(
        friend_a_id=friend_a,
        friend_b_id=friend_b,
        creation_date=datetime.datetime.utcnow()
    )


def get_fake_friendships_by_friendinvite(friendinvite):
    return [
        Friend(
            friend_a_id=friendinvite.requesting_id,
            friend_b_id=friendinvite.requested_id,
            creation_date=datetime.datetime.utcnow()
        ),
        Friend(
            friend_b_id=friendinvite.requesting_id,
            friend_a_id=friendinvite.requested_id,
            creation_date=datetime.datetime.utcnow()
        )
    ]


def get_fake_friendships_by_user(user_id):
    friendship_a = Friend(
        friend_a_id=user_id,
        friend_b_id=9,
        creation_date=datetime.datetime.utcnow()
    )
    return [(friendship_a, "Test Friend")]


def get_fake_userevent(user_id, event_id):
    return UserEvent(
        user_id=user_id,
        event_id=event_id
    )


def get_fake_userevent_from_invite(userinvite):
    return UserEvent(
        user_id=userinvite.invitee_id,
        event_id=userinvite.event_id
    )


def get_fake_events_by_owner(owner_id):
    return [
        Event(
            id=1,
            event_name="Fake Event",
            event_owner_id=owner_id,
            creation_date=datetime.datetime.utcnow(),
            event_date=datetime.datetime.utcnow()
        ),
        Event(
            id=2,
            event_name="Fake Event Two",
            event_owner_id=owner_id,
            creation_date=datetime.datetime.utcnow(),
            event_date=datetime.datetime.utcnow()
        )
    ]


def get_fake_events_by_user(owner_id):
    events = [get_fake_event(1), get_fake_event(2)]
    users = [get_fake_user_by_id(3), get_fake_user_by_id(3)]
    return tuple(zip(users, events))


def get_fake_users_by_event(event_id):
    return [get_fake_user_by_id(1), get_fake_user_by_id(2)]


def get_fake_users_by_emails(emails):
    return [get_fake_user_by_email(email) for email in emails]


def get_fake_event(event_id):
    return Event(
        id=event_id,
        event_name="Fake Event",
        event_owner_id=3,
        creation_date=datetime.datetime.utcnow(),
        event_date=datetime.datetime.utcnow()
    )


def get_fake_user_by_email(email):
    user = User(
        id=5,
        email=email,
        screen_name="Fake User",
        phone="+44(0)1144728913",
        latitude=50.1444,
        longitude=1.25515
    )
    return user


def get_fake_user_by_email_pw(email):
    user = User(
        id=5,
        email=email,
        screen_name="Fake User",
        phone="+44(0)1144728913",
        latitude=50.1444,
        longitude=1.25515
    )
    user.hash_password("fakepassword")
    return user


def get_fake_user_by_id(user_id, pw=False):
    user = User(
        id=user_id,
        email="fakeuser@gmail.com",
        screen_name="Fake User",
        phone="+44(0)1144728913",
        latitude=50.1444,
        longitude=1.25515
    )
    return user


def get_fake_userinvite(invite_id):
    return UserInvite(
        id=invite_id,
        inviter_id=3,
        invitee_id=7,
        event_id=6
    )


def get_fake_userinvites(user_id):
    events = [
        Event(
            id=19,
            event_name="Fake Event",
            event_owner_id=3,
            creation_date=datetime.datetime.utcnow()
        ),
        Event(
            id=21,
            event_name="Another Fake Event",
            event_owner_id=6,
            creation_date=datetime.datetime.utcnow()
        )
    ]
    additional_data = [("Fake Owner", 1, "Fake Owner"),
                       ("Another Fake", 2, "Not The Owner")]
    return [tuple([event, *additional_data[i]])
            for i, event in enumerate(events)]

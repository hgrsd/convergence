import datetime
from convergence.models import Event, User, UserInvite


def get_fake_event(event_id):
    return Event(
        id=event_id,
        event_name="Fake Event",
        event_owner_id=3,
        creation_date=datetime.datetime.utcnow()
    )


def get_fake_user_by_id(user_id):
    user = User(
        id=user_id,
        email="fakeuser@gmail.com",
        screen_name="Fake User",
        phone="+44(0)1144728913",
        latitude=50.1444,
        longitude=1.25515
    )
    user.hash_password("fakepassword")
    return user


def get_fake_user_by_email(email):
    user = User(
        id=12,
        email=email,
        screen_name="Fake User",
        phone="+44(0)1144728913",
        latitude=50.1444,
        longitude=1.25515
    )
    user.hash_password("fakepassword")
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

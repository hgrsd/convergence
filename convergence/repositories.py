"""
repositories.py
Provides data retrieval methods for models used by Convergence.
Wraps SQLAlchemy methods.
"""
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from . import db
from . import exceptions
from .models import User, UserEvent, Event, Place, UserInvite


class Store:

    def __init__(self, session):
        """
        Initialise class instance using session (if provided),
        otherwise create new session.
        :param session: session object or None
        """
        self.session = session if session else db.create_session()


class UserStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def get_user_by_email(self, email):
        """
        Return user for provided email address
        :param email: email address
        :return: User object
        """
        return self.session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, user_id):
        """
        Return user for provided user id
        :param user_id: user id
        :return: User object
        """
        return self.session.query(User).get(user_id)

    def get_users_by_ids(self, user_ids):
        """
        Return users for provided user ids
        :param user_ids: list of user ids
        :return: list of User objects
        """
        return self.session.query(User).filter(User.id.in_(user_ids)).all()

    def add_user(self, user):
        """
        Add user to database
        :param user: User object
        """
        self.session.add(user)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise exceptions.InputError("Email address in use.")
            else:
                raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def delete_user(self, user):
        """
        Delete user from database
        :param user: User object
        """
        self.session.delete(user)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def commit_changes(self):
        """Commit changes in session object to database"""
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            raise exceptions.DatabaseError(f"Error: {str(e)}")


class EventStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def get_event_by_id(self, event_id):
        """
        Return event for provided event id
        :param event_id: event id
        :return: Event object
        """
        return self.session.query(Event).get(event_id)

    def get_events_by_owner(self, user_id):
        """
        Return events owned by user with specified id
        :param user_id: user id
        :return: list of Event objects
        """
        return self.session.query(Event) \
                           .filter_by(event_owner_id=user_id) \
                           .all()

    def get_owner_id(self, event_id):
        """
        Return user_id of user who owns event with event id specified
        :param even_id: event id
        :return: user id of event owner
        """
        event = self.session.query(Event).get(event_id)
        if not event:
            return None
        return event.event_owner_id

    def add_event(self, event):
        """
        Add event to database
        :param event: Event object
        """
        self.session.add(event)
        try:
            self.session.flush()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def delete_event(self, event):
        """
        Delete event from database
        :param event: Event object
        """
        self.session.delete(event)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None


class UserEventStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def get_events_by_user(self, user_id):
        """
        Return all events for specified user
        :param user_id: user id
        :return: list of tuples(User object, Event object)
                 where the User object is the event owner
        """
        return self.session.query(User, Event) \
                           .join(Event) \
                           .join(UserEvent) \
                           .filter(UserEvent.user_id == user_id) \
                           .all()

    def get_users_by_event(self, event_id):
        """
        Return all members of a specified event
        :param event_id: event id
        :return: list of User objects
        """
        return self.session.query(User) \
                           .join(UserEvent, User.userevents) \
                           .filter(UserEvent.event_id == event_id) \
                           .all()

    def get_userevent(self, user_id, event_id):
        """
        Return UserEvent by (user id, event id)
        :param user_id: user id
        :param event_id: event id
        :return: UserEvent object
        """
        return self.session.query(UserEvent) \
                   .filter_by(user_id=user_id, event_id=event_id) \
                   .first()

    def add_userevent(self, userevent):
        """
        Add UserEvent to database
        :param userevent: UserEvent object
        """
        self.session.add(userevent)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def delete_userevent(self, userevent):
        """
        Delete UserEvent from database
        :param userevent: UserEvent object
        """
        self.session.delete(userevent)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None


class UserInviteStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def add_userinvite(self, userinvite):
        """
        Add UserInvite to database
        :param userinvite: UserInvite object
        """
        self.session.add(userinvite)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def get_invitation_by_id(self, invite_id):
        """
        Return invitation by id
        :param invite_id: invite id
        :return: UserInvite object
        """
        return self.session.query(UserInvite).get(invite_id)

    def get_invitations_by_user(self, user_id):
        """
        Return all pending invitations for specified user
        :param user_id: user id
        :return: list of tuples(Event, Event owner's screen name,
                                UserInvite's id, inviter's screen name)
                 for each pending invite, where Event is an Event object,
                 both screen names are strings, and the UserInvite id is an int
        """
        event_owner = sa.alias(User)
        inviter = sa.alias(User)
        return self.session.query(Event,
                                  event_owner.c.screen_name,
                                  UserInvite.id,
                                  inviter.c.screen_name) \
                           .join(UserInvite, Event.userinvites) \
                           .join(event_owner, Event.event_owners) \
                           .join(inviter, UserInvite.inviter_ids) \
                           .filter(UserInvite.invitee_id == user_id) \
                           .all()

    def delete_userinvite(self, userinvite):
        """
        Delete UserInvite from database
        :param userinvite: UserInvite object
        """
        self.session.delete(userinvite)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None


class PlaceStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def get_places_around_point(self, point, radius):
        """
        Return a list of places around a specified point,
        within a specified radius.
        :param point: Point object
        :param radius: radius in metres
        :return: list of Place objects
        """
        return self.session.query(Place) \
                           .filter(Place.within_range(point, radius))

    def add_place(self, place):
        """
        Add Place to database
        :param place: Place object
        """
        self.session.add(place)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

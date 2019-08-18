import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from convergence.utils import exceptions
from convergence.data.repo import Store
from convergence.data.models import User, UserInvite, Event


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

    def add_userinvites(self, userinvites):
        """
        Add multiple UserInvite objects to a database
        :param userinvites: UserInvite objects
        """
        try:
            self.session.bulk_save_objects(userinvites)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def get_invite_by_id(self, invite_id):
        """
        Return invite by id
        :param invite_id: invite id
        :return: UserInvite object
        """
        return self.session.query(UserInvite).get(invite_id)

    def get_invites_by_user(self, user_id):
        """
        Return all pending invites for specified user
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
                           .join(UserInvite, Event.rel_userinvites) \
                           .join(event_owner, Event.rel_event_owners) \
                           .join(inviter, UserInvite.rel_inviter_ids) \
                           .filter(UserInvite.invitee_id == user_id) \
                           .all()

    def get_invite_by_details(self, user_id, event_id):
        """
        Return pending invites, if they exist, based on the
        specified user_id and event_id.
        :param user_id: user id
        :param event_id: event id
        :return: UserInvite, else None
        """
        return self.session.query(UserInvite) \
                   .filter(UserInvite.invitee_id == user_id,
                           UserInvite.event_id == event_id) \
                   .first()

    def get_users_by_event(self, event_id):
        """
        Return all members who have a pending invite to an event
        :param event_id: event id
        :return: list of User objects
        """
        return self.session.query(User) \
                           .join(UserInvite.rel_invitee_ids) \
                           .filter(UserInvite.event_id == event_id) \
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

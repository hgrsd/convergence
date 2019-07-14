import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from convergence import exceptions
from convergence.repo import Store
from convergence.models import User, UserInvite, Event


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

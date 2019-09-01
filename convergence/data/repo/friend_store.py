import sqlalchemy as sa
import datetime
from sqlalchemy.exc import SQLAlchemyError

from convergence.utils import exceptions
from convergence.utils import logger
from convergence.data.repo import Store
from convergence.data.models import User, Friend, FriendInvite


class FriendStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def add_friendinvite(self, friendinvite):
        """
        Add FriendInvite to database
        :param userinvite: FriendInvite object
        """
        self.session.add(friendinvite)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            logger.log_error(f"Database Error: {str(e)}")
            self.session.rollback()
            raise exceptions.ServerError("Error adding invite")
        return None

    def add_friendinvites(self, friendinvites):
        """
        Add multiple FriendInvite objects to a database
        :param userinvites: sequence of FriendInvite objects
        """
        try:
            self.session.bulk_save_objects(friendinvites)
            self.session.commit()
        except SQLAlchemyError as e:
            logger.log_error(f"Database Error: {str(e)}")
            self.session.rollback()
            raise exceptions.ServerError("Error adding invites")
        return None

    def get_friendships_by_user(self, user_id):
        return self.session.query(Friend, User.screen_name) \
                           .join(User, Friend.rel_friend_b_ids) \
                           .filter(Friend.friend_a_id == user_id) \
                           .all()

    def get_invite_by_id(self, invite_id):
        """
        Return invite by id
        :param invite_id: invite id
        :return: FriendInvite object
        """
        return self.session.query(FriendInvite).get(invite_id)

    def get_pending_invites_received(self, user_id):
        """
        Return all pending invites for specified user
        :param user_id: user id
        :return: list of tuples(FriendInvite, User)
        for each pending invite, where User is the requesting user
        """
        return self.session.query(FriendInvite, User) \
                           .join(User, FriendInvite.rel_requesting_ids) \
                           .filter(FriendInvite.requested_id == user_id) \
                           .all()

    def get_pending_invites_sent(self, user_id):
        """
        Return all pending invites sent by user_id
        :param user_id: user id
        :return: pending FriendInvites
        """
        return self.session.query(FriendInvite) \
                           .filter(FriendInvite.requesting_id == user_id) \
                           .all()

    def add_friendship_from_invite(self, friendinvite):
        """
        Add friendship to db from friendinvite passed in and
        remove friendinvite from db.
        :param friendinvite: FriendInvite object
        :return: both Friend objects
        """
        a_to_b = Friend(
            friend_a_id=friendinvite.requesting_id,
            friend_b_id=friendinvite.requested_id,
            creation_date=datetime.datetime.utcnow()
        )
        b_to_a = Friend(
            friend_a_id=friendinvite.requested_id,
            friend_b_id=friendinvite.requesting_id,
            creation_date=datetime.datetime.utcnow()
        )
        try:
            self.session.bulk_save_objects([a_to_b, b_to_a])
            self.session.delete(friendinvite)
            self.session.commit()
        except SQLAlchemyError as e:
            logger.log_error(f"Database Error: {str(e)}")
            self.session.rollback()
            raise exceptions.ServerError("Error adding friendship")
        return (a_to_b, b_to_a)

    def add_friendship(self, friend_a_id, friend_b_id):
        """
        Add friendship to db.
        :param friend_a_id: user id
        :param friend_b_id: user id
        :return: both Friend objects (Friendship is reflexive)
        """
        a_to_b = Friend(
            friend_a_id=friend_a_id,
            friend_b_id=friend_b_id,
            creation_date=datetime.datetime.utcnow()
        )
        b_to_a = Friend(
            friend_a_id=friend_b_id,
            friend_b_id=friend_a_id,
            creation_date=datetime.datetime.utcnow()
        )
        try:
            self.session.bulk_save_objects([a_to_b, b_to_a])
            self.session.commit()
        except SQLAlchemyError as e:
            logger.log_error(f"Database Error: {str(e)}")
            self.session.rollback()
            raise exceptions.ServerError("Error adding friendship")
        return (a_to_b, b_to_a)

    def delete_friendship(self, friend_a_id, friend_b_id):
        """
        Delete Friend
        :param friend_a_id: user id
        :param friend_b_id: user id
        """
        self.session.query(Friend) \
                    .filter(sa.or_(
                        sa.and_(
                            Friend.friend_a_id == friend_a_id,
                            Friend.friend_b_id == friend_b_id
                        ),
                        sa.and_(
                            Friend.friend_a_id == friend_b_id,
                            Friend.friend_b_id == friend_a_id
                        )
                        )
                     ) \
                    .delete()
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            logger.log_error(f"Database Error: {str(e)}")
            self.session.rollback()
            raise exceptions.ServerError("Error deleting friendship")
        return None

    def delete_friendinvite(self, friendinvite):
        """
        Delete FriendInvite from database
        :param userinvite: FriendInvite object
        """
        self.session.delete(friendinvite)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            logger.log_error(f"Database Error: {str(e)}")
            self.session.rollback()
            raise exceptions.ServerError("Error deleting invite")
        return None

    def get_invite_by_details(self, requesting_id, requested_id):
        """
        Return pending invite, if it exists, based on the
        specified requesting_id and requested_id.
        :param requesting_id: user id of friendship proposer
        :param requested_id: user whose friendship is requested
        :return: FriendInvite, else None
        """
        return self.session.query(FriendInvite) \
                   .filter(FriendInvite.requesting_id == requesting_id,
                           FriendInvite.requested_id == requested_id) \
                   .first()

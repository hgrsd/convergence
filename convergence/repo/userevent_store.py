from sqlalchemy.exc import SQLAlchemyError

from convergence import exceptions
from convergence.repo import Store
from convergence.models import Event, User, UserEvent


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
                           .join(UserEvent, User.rel_userevents) \
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

    def add_user_to_event_from_invite(self, userinvite):
        """
        Add user to event based on passed-in userinvite,
        then delete userinvite
        """
        userevent = UserEvent(
            user_id=userinvite.invitee_id,
            event_id=userinvite.event_id
        )
        try:
            self.session.add(userevent)
            local_object = self.session.merge(userinvite)  # merge into session
            self.session.delete(local_object)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return userevent

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

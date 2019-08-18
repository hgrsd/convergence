from sqlalchemy.exc import SQLAlchemyError

from convergence.utils import exceptions
from convergence.data.repo import Store
from convergence.data.models import Event


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
            self.session.commit()
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

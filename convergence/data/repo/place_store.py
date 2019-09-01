from sqlalchemy.exc import SQLAlchemyError

from convergence.utils import exceptions
from convergence.utils import logger
from convergence.data.repo import Store
from convergence.data.models import Place


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
                           .filter(Place.within_range(point, radius)) \
                           .all()

    def add_place(self, place):
        """
        Add Place to database
        :param place: Place object
        """
        self.session.add(place)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            logger.log_error(
                f"Database Error while adding place: {str(e)}"
            )
            self.session.rollback()
        return None

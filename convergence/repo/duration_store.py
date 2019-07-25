import datetime
from sqlalchemy.exc import SQLAlchemyError

from convergence import exceptions
from convergence.repo import Store
from convergence.models import DurationCycle, DurationDrive, DurationTransit, \
                               DurationWalk


models = {
    "driving": DurationDrive,
    "bicycling": DurationCycle,
    "walking": DurationWalk,
    "transit": DurationTransit
}


class DurationStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def get_nearby_coordinates(self, point, mode, radius):
        model = models[mode]
        return self.session.query(model.lat_a, model.long_a) \
                           .filter(model.within_range(point, radius)) \
                           .all()

    def get_travel_time(self, point_a, point_b, mode):
        model = models[mode]
        return self.session.query(model.duration) \
                           .filter(
                               model.lat_a == point_a.lat,
                               model.long_a == point_a.long,
                               model.lat_b == point_b.lat,
                               model.long_b == point_b.long
                           ).first()

    def update_duration(self, point_a, point_b, duration, mode):
        model = models[mode]
        already_known = self.session.query(model) \
                                    .filter(
                                        model.lat_a == point_a.lat,
                                        model.long_a == point_a.long,
                                        model.lat_b == point_b.lat,
                                        model.long_b == point_b.long
                                    ).first()
        if already_known:
            already_known.duration = duration
            already_known.timestamp = datetime.datetime.utcnow()
            self.session.add(already_known)
            self.session.commit()
            return already_known
        else:
            a_to_b = model(
                lat_a=point_a.lat,
                long_a=point_a.long,
                lat_b=point_b.lat,
                long_b=point_b.long,
                duration=duration,
                timestamp=datetime.datetime.utcnow()
            )
            self.session.add(a_to_b)
            self.session.commit()
            return a_to_b

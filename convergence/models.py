import math
import sqlalchemy as sa

from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext import declarative
from passlib.apps import custom_app_context as pwd_context

from .point import Point

base = declarative.declarative_base()


class User(base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(32), unique=True, nullable=False)
    email = sa.Column(sa.String(254), unique=True, nullable=False)
    phone_number = sa.Column(sa.String(25), unique=True, nullable=False)
    password_hash = sa.Column(sa.String(128))
    last_seen_lat = sa.Column(sa.Float)
    last_seen_long = sa.Column(sa.Float)

    userevent = sa.orm.relation("UserEvent")
    event = sa.orm.relation("Event")

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def basic_info(self):
        return {"id": self.id, "username": self.username}

    def get_location(self):
        return Point(self.last_seen_lat, self.last_seen_long)

    def full_info(self):
        """ Return all info except for password hash """
        return {"id": self.id, "username": self.username,
                "email": self.email,
                "phone": self.phone_number,
                "last_seen_lat": self.last_seen_lat,
                "last_seen_long": self.last_seen_long}


class Event(base):
    __tablename__ = "events"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128))
    owner = sa.Column(sa.ForeignKey("users.id", ondelete="CASCADE"),
                      index=True)
    creation_date = sa.Column(sa.DateTime)

    userevent = sa.orm.relation("UserEvent")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserEvent(base):
    __tablename__ = "userevents"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.ForeignKey("users.id", ondelete="CASCADE"),
                        index=True)
    event_id = sa.Column(sa.ForeignKey("events.id", ondelete="CASCADE"),
                         index=True)
    __table_args__ = (sa.UniqueConstraint("user_id", "event_id"),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Place(base):
    __tablename__ = "places"
    id = sa.Column(sa.Integer, primary_key=True)
    gm_id = sa.Column(sa.String(), unique=True)
    name = sa.Column(sa.String(128), index=True)
    lat = sa.Column(sa.Float)
    long = sa.Column(sa.Float)
    gm_price = sa.Column(sa.Integer)
    gm_rating = sa.Column(sa.Float)
    gm_types = sa.Column(sa.ARRAY(sa.String()))
    address = sa.Column(sa.String(128))
    timestamp = sa.Column(sa.DateTime)

    @hybrid_method
    def within_range(self, point, radius):
        """Check whether point is within radius of self."""
        self_lat = math.radians(self.lat)
        self_long = math.radians(self.long)
        other_lat = math.radians(point[0])
        other_long = math.radians(point[1])
        R = 6371
        dist = math.acos(math.sin(self_lat) * math.sin(other_lat)
                         + math.cos(self_lat) * math.cos(other_lat)
                         * math.cos(self_long - other_long)) * R
        return dist < radius / 1000  # radius in metres, convert to km

    @within_range.expression
    def within_range(cls, point, radius):
        """SQL-expression version of within_range"""
        self_lat = sa.func.radians(cls.lat)
        self_long = sa.func.radians(cls.long)
        other_lat = sa.func.radians(point.lat)
        other_long = sa.func.radians(point.long)
        R = 6371
        dist = sa.func.acos(sa.func.sin(self_lat) * sa.func.sin(other_lat)
                            + sa.func.cos(self_lat) * sa.func.cos(other_lat)
                            * sa.func.cos(self_long - other_long)) * R
        return dist < radius / 1000  # radius in metres, convert to km

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

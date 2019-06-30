import math
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy import func

from . import db
from .point import Point


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen_lat = db.Column(db.Float)
    last_seen_long = db.Column(db.Float)
    available = db.Column(db.Boolean)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def basic_info(self):
        return {"id": self.id, "username": self.username}

    def get_location(self):
        return Point(self.last_seen_lat, self.last_seen_long)

    def full_info(self):
        """ Return all info except for password hash """
        return {"id": self.id, "username": self.username,
                "last_seen_lat": self.last_seen_lat,
                "last_seen_long": self.last_seen_long,
                "available": self.available}


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    owner = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"),
                      index=True)
    creation_date = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserEvent(db.Model):
    __tablename__ = "userevents"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"),
                        index=True)
    event_id = db.Column(db.ForeignKey("events.id", ondelete="CASCADE"),
                         index=True)
    __table_args__ = (db.UniqueConstraint("user_id", "event_id"),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Place(db.Model):
    __tablename__ = "places"
    id = db.Column(db.Integer, primary_key=True)
    gm_id = db.Column(db.String(), unique=True)
    name = db.Column(db.String(128), index=True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    gm_price = db.Column(db.Integer)
    gm_rating = db.Column(db.Float)
    gm_types = db.Column(db.ARRAY(db.String()))
    address = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)

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
        self_lat = func.radians(cls.lat)
        self_long = func.radians(cls.long)
        other_lat = func.radians(point.lat)
        other_long = func.radians(point.long)
        R = 6371
        dist = func.acos(func.sin(self_lat) * func.sin(other_lat)
                         + func.cos(self_lat) * func.cos(other_lat)
                         * func.cos(self_long - other_long)) * R
        return dist < radius / 1000  # radius in metres, convert to km

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

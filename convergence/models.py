import math
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy import func
from sqlalchemy.ext import declarative
from sqlalchemy import Column, Float, String, Integer, DateTime, \
                       ForeignKey, UniqueConstraint, Boolean, ARRAY

from .point import Point

base = declarative.declarative_base()


class User(base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    phone_number = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen_lat = db.Column(db.Float)
    last_seen_long = db.Column(db.Float)

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
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    owner = Column(ForeignKey("users.id", ondelete="CASCADE"),
                   index=True)
    creation_date = Column(DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserEvent(base):
    __tablename__ = "userevents"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"),
                     index=True)
    event_id = Column(ForeignKey("events.id", ondelete="CASCADE"),
                      index=True)
    __table_args__ = (UniqueConstraint("user_id", "event_id"),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Place(base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True)
    gm_id = Column(String(), unique=True)
    name = Column(String(128), index=True)
    lat = Column(Float)
    long = Column(Float)
    gm_price = Column(Integer)
    gm_rating = Column(Float)
    gm_types = Column(ARRAY(String()))
    address = Column(String(128))
    timestamp = Column(DateTime)

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

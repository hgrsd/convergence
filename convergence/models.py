from . import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen_lat = db.Column(db.Float)
    last_seen_long = db.Column(db.Float)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    owner = db.Column(db.ForeignKey('users.id', ondelete="CASCADE"))


class UserGroup(db.Model):
    __tablename__ = 'usergroups'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id', ondelete="CASCADE"), index=True)
    group_id = db.Column(db.ForeignKey('groups.id', ondelete="CASCADE"), index=True)
    __table_args__ = (db.UniqueConstraint('user_id', 'group_id'),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Place(db.Model):
    __tablename__ = 'places'
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


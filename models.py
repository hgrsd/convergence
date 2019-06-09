from convergence import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    owner = db.Column(db.ForeignKey('users.id'))


class UserGroup(db.Model):
    __tablename__ = 'usergroups'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), index=True)
    group_id = db.Column(db.ForeignKey('groups.id'), index=True)
    __table_args__ = (db.UniqueConstraint('user_id', 'group_id'),)

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    coordinates = db.Column(db.ARRAY(db.Integer, True, 2))

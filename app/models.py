from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(32))
    bio = db.Column(db.String(512))
    quota = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(32))
    desc = db.Column(db.String(128))
    tag = db.Column(db.String(16))

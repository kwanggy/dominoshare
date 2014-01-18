from datetime import datetime
import uuid, OpenSSL

from flask import *
from flask.ext.sqlalchemy import SQLAlchemy


from . import app, db

from util import totimestamp


class User(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, unique=True)
    pw = db.Column(db.String)
    session_key = db.Column(db.String, db.ForeignKey('session.key'))
    session = db.relationship('Session',
        backref=db.backref('user', lazy='dynamic'))
    rid = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room',
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, phone, pw):
        self.created_at = datetime.utcnow()
        self.phone = phone
        self.pw = pw
        self.room = None

    def join_room(self, room):
        if len(room.users.all()) > 2:
            return False
        self.room = room
        room.updated()
        return True

    def leave_room(self, room):
        self.room = None
        room.updated()

    def set_session(self, session):
        if self.session:
            db.session.delete(self.session)
        self.session = session
        

class Session(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)

    def __init__(self):
        self.created_at = datetime.utcnow()
        self.key = str(uuid.UUID(bytes = OpenSSL.rand.bytes(16)))

class Room(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    zipcode = db.Column(db.String)
    menu = db.Column(db.String)
    photo_url = db.Column(db.String)
    last_updated = db.Column(db.DateTime)

    def __init__(self, title, zipcode, menu):
        self.created_at = datetime.utcnow()
        self.title = title
        self.zipcode = zipcode
        self.menu = menu
        self.photo_url = ''
        self.updated()

    def updated(self):
        self.last_updated = datetime.utcnow()

    def to_json(self):
        ts = totimestamp(self.last_updated)
        app.last_updated[self.id] = ts
        j = {
            'id': self.id,
            'title': self.title,
            'zipcode': self.zipcode,
            'menu': self.menu,
            'photo_url': self.photo_url,
            'users': [u.phone for u in self.users],
            'last_updated': ts
        }
        return j

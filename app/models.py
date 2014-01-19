from datetime import datetime
import uuid, OpenSSL

from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy


from . import app, db

from util import totimestamp


class User(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, unique=True)
    pw_hash = db.Column(db.String)
    session_key = db.Column(db.String, db.ForeignKey('session.key'))
    session = db.relationship('Session',
        backref=db.backref('user', lazy='dynamic'))
    rid = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room',
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, phone, pw):
        self.created_at = datetime.utcnow()
        self.phone = phone
        self.pw_hash = generate_password_hash(pw)
        self.room = None

    def join_room(self, room):
        self.leave_room()
        if len(room.users.all()) > 2:
            return False
        self.room = room
        room.updated()
        return True

    def leave_room(self):
        if self.room == None:
            return
        room = self.room
        self.room = None
        if len(room.users.all()) > 0:
            room.updated()
        else:
            db.session.delete(room)

    def set_session(self, session):
        if self.session:
            db.session.delete(self.session)
        self.session = session

    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)
        

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
        self.set_menu(menu)
        self.updated()

    def set_menu(self, menu):
        self.menu = menu
        menu = menu.lower()

        if 'wing' in menu:
            url = 'https://cache.dominos.com/nolo/us/en/013153/assets/build/images/img/products/thumbnails/S_BONEIN.jpg'
        elif 'boneless' in menu:
            url = 'https://cache.dominos.com/nolo/us/en/013153/assets/build/images/img/products/thumbnails/S_BONELESS.jpg'
        elif 'pasta' in menu:
            url = 'https://cache.dominos.com/nolo/us/en/013153/assets/build/images/img/products/thumbnails/S_BUILD.jpg'
        elif 'pizza' in menu:
            url = 'https://cache.dominos.com/nolo/us/en/013153/assets/build/images/img/products/thumbnails/S_PIZZA.jpg'
        else:
            url = 'https://cache.dominos.com/nolo/us/en/013153/assets/build/images/img/img-logo-home.png'

        self.photo_url = url

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

import json

from flask import *
from functools import update_wrapper

from . import app, db
from .models import User, Session
from .config import conf
from util import log


def json_response():
    def decorator(f):
        def wrapped():
            try:
                res = f()
            except Exception as e:
                return jsonify({
                    'status_code': 404 if request.method == 'GET' else 400,
                    'error': str(e)
                })
            return jsonify({
                'status_code': 200,
                'result': res
            })
        return update_wrapper(wrapped, f)
    return decorator

def newSessionKey(user):
    s = Session(user)
    db.session.add(s)
    db.session.commit()
    return user.session.first().key
    

@app.route('/reset')
@json_response()
def reset():
    for u in User.query.all():
        for s in u.session.all():
            db.session.delete(s)
        db.session.delete(u)
    db.session.commit()
    return len(User.query.all())
    

@app.route('/signup', methods=['POST'])
@json_response()
def signup_page():
    if 'phone' not in request.form:
        raise Exception('phone number is required')
    phone = request.form['phone']

    if 'pass' not in request.form:
        raise Exception('password is required')
    pw = request.form['pass']
    
    u = User(phone, pw)
    db.session.add(u)
    db.session.commit()

    return newSessionKey(u)


@app.route('/signin', methods=['POST'])
@json_response()
def signin_page():
    if 'phone' not in request.form:
        raise Exception('phone number is required')
    phone = request.form['phone']

    if 'pass' not in request.form:
        raise Exception('password is required')
    pw = request.form['pass']

    u = User.query.filter_by(phone=phone).first()
    if u == None:
        raise Exception('phone number is not matching')
    if u.pw != pw:
        raise Exception('password is not matching')

    return newSessionKey(u)


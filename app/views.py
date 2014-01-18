import json
import traceback

from flask import *
from functools import update_wrapper

from . import app, db
from .models import User, Session, Room
from .config import conf
from util import log


def json_response():
    def decorator(f):
        def wrapped():
            try:
                log(request.args)
            except:
                pass
            try:
                log(request.form)
            except:
                pass
            try:
                res = f()
            except Exception as e:
                log(traceback.format_exc())
                status_code = 404 if request.method == 'GET' else 400
                return jsonify({
                    'status_code': status_code,
                    'error': str(e)
                }), 200 # status_code
            return jsonify({
                'status_code': 200,
                'result': res
            })
        return update_wrapper(wrapped, f)
    return decorator

def session_required():
    def decorator(f):
        def wrapped():
            if request.method == 'GET':
                key = request.args.get('session_key', None)
            elif request.method == 'POST':
                key = request.form.get('session_key', None)
            if key == None:
                raise Exception('session key is required')

            s = Session.query.filter_by(key=key).first()
            if s == None:
                raise Exception('session key is not valid')
            if s.user == None:
                log('****', 'session is not valid', s.id)
                raise Exception('session is not valid')
            return f(s.user.first())
        return update_wrapper(wrapped, f)
    return decorator

def userinfo_required(create=False):
    def decorator(f):
        def wrapped():
            if 'phone' not in request.form:
                raise Exception('phone number is required')
            phone = request.form['phone']

            if 'pass' not in request.form:
                raise Exception('password is required')
            pw = request.form['pass']
            if create:
                u = User(phone, pw)
                db.session.add(u)
                db.session.commit()
            else:
                u = User.query.filter_by(phone=phone).first()
                if u == None:
                    raise Exception('phone number does not exist')
                if u.pw != pw:
                    raise Exception('password does not match')
            return f(u)
        return update_wrapper(wrapped, f)
    return decorator
    

def newSessionKey(user):
    s = Session()
    user.set_session(s)
    db.session.add(s)
    db.session.commit()
    return user.session_key


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/api/reset')
@json_response()
def reset():
    try: 
        if not conf['sys']['test-mode']:
            db.engine.execute('DROP TABLE "user" CASCADE')
            db.engine.execute('DROP TABLE "session" CASCADE')
            db.engine.execute('DROP TABLE "room" CASCADE')
        else:
            db.drop_all()
    except:
        pass
    db.create_all()
    return len(User.query.all())
    

@app.route('/api/signup', methods=['POST'])
@json_response()
@userinfo_required(create=True)
def signup_page(user):
    return newSessionKey(user)


@app.route('/api/signin', methods=['POST'])
@json_response()
@userinfo_required()
def signin_page(user):
    return newSessionKey(user)


@app.route('/api/room', methods=['GET', 'POST'])
@json_response()
@session_required()
def room_page(user):
    if request.method == 'GET':
        if 'zipcode' in request.args:
            zipcode = request.args['zipcode']
            rooms = Room.query.filter_by(zipcode=zipcode).all()
            res = []
            for r in rooms:
                if len(r.users) == 1:
                    res.append(r.to_json())
            return res
        elif 'id' in request.args and 'last_updated' in request.args:
            lu = float(request.args['last_updated'])
            rid = request.args['id']
            if lu < app.last_updated[rid]:
                r = Room.query.filter_by(id=rid).first()
                res = r.to_json()
                return res
            return None
        else:
            raise Exception('invalid arguments')
    elif request.method == 'POST':
        if 'id' in request.form:
            rid = request.form['id']
            r = Room.query.filter_by(id=rid).first()
            if r == None:
                raise Exception('room id does not exist')
            user.join_room(r)
            db.session.commit()
            res = r.to_json()
            return res
        elif 'title' in request.form \
             and 'zipcode' in request.form \
             and 'menu' in request.form:
            title =  request.form['title']
            zipcode =  request.form['zipcode']
            menu =  request.form['menu']
            r = Room(title, zipcode, menu)
            db.session.add(r)
            user.join_room(r)
            db.session.commit()
            res = r.to_json()
            return res
        elif 'leave' in request.form:
            user.leave_room()
        else:
            raise Exception('invalid arguments')

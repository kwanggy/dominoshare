from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from util import log
from config import conf, load_default_conf


load_default_conf()
app = Flask(__name__)
app.config['DEBUG'] = conf['sys']['debug']
app.config['SECRET_KEY'] = conf['sys']['secret_key']
db = conf['sys']['database']
if '://' not in conf['sys']['database']:
    import os
    db = os.environ[db]
app.config['SQLALCHEMY_DATABASE_URI'] = db
db = SQLAlchemy(app)


from . import models, views

db.create_all()

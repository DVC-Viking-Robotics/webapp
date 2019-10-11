"""A module to manage user accounts"""

# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name

import pymysql
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin, LoginManager

app = Flask(__name__)

# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://UserAdmin:^0o9JpRAPazf@webapp-dev-db.c1cjueiaoepn.us-west-1.rds.amazonaws.com:3306/user.accounts'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['LOGIN_DISABLED'] = False

db = SQLAlchemy(app)
   
   
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
login_manager.login_message_category = "warning"

class Remote:
    """A class used for instantiating a user's saved remote control configurations.
        There should be 1 object of this class type per remote control.

    """
    def __init__(self, name, link='/remote'):
        self.name = name
        self.link = link

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id',db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    
    def __init__(self, username,password):
        self.username = username
        self.password = password
         
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)
        
class AnonUser(AnonymousUserMixin):
    """A class for instantiating an anonymous user account.
        There should be only 1 object of this class type.

    .. note:: This may get deprecated for security concerns/simplicity.

    """
    def __init__(self):
        self._id = 'anonymous'
        self._remotes = []
        self._config = {}

    @property
    def get_id(self):
        """This class attrubute holds the user account's ID"""
        return self._id


@login_manager.user_loader
def load_user(user_id):
    """A function wrapper to retreive a user account's object"""
    return User.query.get(int(user_id))

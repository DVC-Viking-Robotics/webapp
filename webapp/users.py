"""A module to manage user accounts"""

# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name

import pymysql
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .config import DISABLE_DATABASE

if not DISABLE_DATABASE:
    db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message_category = "warning"


class Remote:
    """
    A class used for instantiating a user's saved remote control configurations.
    There should be 1 object of this class type per remote control.
    """

    def __init__(self, name, link='/remote'):
        self.name = name
        self.link = link

if not DISABLE_DATABASE:
    # pylint: disable=no-member
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column('user_id', db.Integer, primary_key=True, index=True)
        username = db.Column('username', db.String(20), unique=True)
        password = db.Column('password', db.String(20))

        def __init__(self, username, password):
            # Note: The primary key (id) is auto-generated
            self.username = username
            self.password = password

        def is_authenticated(self):
            return True

        def is_active(self):
            return True

        def is_anonymous(self):
            return False

        def get_id(self):
            """This class attrubute holds the user account's ID"""
            return str(self.id)
    # pylint: enable=no-member

@login_manager.user_loader
def load_user(user_id):
    """A function wrapper to retreive a user account's object"""
    if not DISABLE_DATABASE:
        return User.query.get(int(user_id))
    else:
        return 42

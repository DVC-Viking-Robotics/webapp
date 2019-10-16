"""
A module to manage user accounts
"""

# pylint: disable=invalid-name

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message_category = "warning"

DB = SQLAlchemy()

class User(DB.Model):
    """ A User class for representing a user connected via an SQL database.
    See `"Declaring Models" of the Flask-SQLAlchemy docs
    <https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#declaring-models>`_
    for more info on this class' base object."""

    __tablename__ = 'users'
    id = DB.Column('user_id', DB.Integer, primary_key=True, index=True)
    username = DB.Column('username', DB.String(20), unique=True)
    password = DB.Column('password', DB.String(20))

    def __init__(self, username, password):
        # Note: The primary key (id) is auto-generated
        self.username = username
        self.password = password

    def is_authenticated(self):
        # TODO: This should not always be true
        """ Return true if the user is authenticated. """
        return True

    def is_active(self):
        """ Return true if the user is activated. """
        # TODO: This should not always be true
        return True

    def is_anonymous(self):
        """ Return true if the user is anonymous. """
        return False

    def get_id(self):
        """This class attrubute holds the user account's ID"""
        return str(self.id)

    def __repr__(self):
        return f"<User '{self.username}' of ID {self.id}>"

@login_manager.user_loader
def load_user(user_id):
    """A function wrapper to retreive a user account's object"""
    return User.query.get(int(user_id))

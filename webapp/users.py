"""
A module to manage user accounts
"""

# pylint: disable=invalid-name

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import DISABLE_AUTH_SYSTEM

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message_category = "warning"


"""
A class used for instantiating a user's saved remote control configurations.
There should be 1 object of this class type per remote control.
"""
class Remote:
    def __init__(self, name, link='/remote'):
        self.name = name
        self.link = link

if not DISABLE_AUTH_SYSTEM:
    db = SQLAlchemy()

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

@login_manager.user_loader
def load_user(user_id):
    """A function wrapper to retreive a user account's object"""
    if not DISABLE_AUTH_SYSTEM:
        return User.query.get(int(user_id))
    else:
        return 42

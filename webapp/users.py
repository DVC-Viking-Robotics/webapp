"""A module to manage user accounts"""

# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name

from flask_login import UserMixin, AnonymousUserMixin, LoginManager

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message_category = "warning"

class Remote:
    """A class used for instantiating a user's saved remote control configurations.
    There should be 1 object of this class type per remote control.
    """
    def __init__(self, name, link='/remote'):
        self.name = name
        self.link = link

class User(UserMixin):
    """A class for instantiating saved user accounts.
    There should be 1 object of this class type per user account.
    """
    def __init__(self, name):
        self._id = name
        self._remotes = []
        self._config = {}
        self._load_config()

    def get_id(self):
        """This class attrubute holds the user account's ID"""
        return self._id

    def _load_config(self):
        """This function will load the information about a user's preferences
        (including account settings and remote control configurations) from the backup json
        file titled with the self._id attribute.
        """
        try:
            with open('backup\\{}.json'.format(self._id), 'r') as acct_file:
                for line in acct_file.readlines():
                    # import from json to self.remotes & self.config
                    print(line)
        except OSError:
            pass # file doesn't exist

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

users = {'admin': User(u'admin'), 'anonymous': AnonUser()}
# users['admin'].remotes.append(Remote('dummy remote'))

@login_manager.user_loader
def load_user(user_id):
    """A function wrapper to retreive a user account's object"""
    return users.get(user_id)

from flask_login import UserMixin, AnonymousUserMixin, LoginManager

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message_category = "warning"

class Remote:
    def __init__(self, name, link='/remote'):
        self.name = name
        self.link = link

class User(UserMixin):
    def __init__(self, name):
        self.id = name
        self.remotes = []
        self.config = {}
        self._load_config()

    def get_id(self):
        return self.id

    def _load_config(self):
        try:
            with open('backup\\{}.json'.format(self.id), 'r') as acct_file:
                for line in acct_file.readlines():
                    # import from json to self.remotes & self.config
                    print(line)
        except OSError:
            pass # file doesn't exist

class AnonUser(AnonymousUserMixin):
    def __init__(self):
        self.id = 'anonymous'
        self.remotes = []
        self.config = {}

    def get_id(self):
        return self.id

users = {'admin': User(u'admin'), 'anonymous': AnonUser()}
users['admin'].remotes.append(Remote('dummy remote'))

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

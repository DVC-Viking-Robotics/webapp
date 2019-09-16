# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

from flask import Blueprint, render_template, request, flash, redirect
from flask_login import  login_required, login_user, logout_user
from .users import users, User

blueprint = Blueprint('blueprint', __name__)

@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page"""
    if request.method == 'POST':
        form = request.form
        user_name = form.get('username', default=None)
        is_new = bool(form.get('register', default=False))
        if user_name is not None:
            if bool(users.get(user_name)) or is_new: # login
                if is_new and not bool(users.get(user_name)): # add new user
                    users[user_name] = User(user_name)
                    flash('Account created successfully.', 'info')
                if users.get(user_name):
                    login_user(users.get(user_name))
                    flash('Logged in successfully.', 'success')
                    return redirect('remote')
            else:
                flash('Username "{}" does not exist!'.format(user_name), 'error')
    return render_template('login.html')

@blueprint.route("/logout")
def logout():
    """Redirects to login page after logging out"""
    logout_user()
    return redirect("login")

@blueprint.route('/')
@blueprint.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home')

@blueprint.route('/remote')
@login_required
def remote():
    return render_template('remote.html', title='Remote Control')

@blueprint.route('/camera')
@login_required
def camera():
    return render_template('camera.html', title='Live Camera feed')

@blueprint.route('/sensors')
@login_required
def sensors():
    return render_template('sensors.html', title='Sensor Dashboard')

@blueprint.route('/automode')
@login_required
def automode():
    return render_template('automode.html', title='Autonomous Navigation')

@blueprint.route('/settings')
@login_required
def settings_page():
    return render_template('settings.html', title='Settings')

@blueprint.route('/about')
def about():
    return render_template('about.html', title='About this project')

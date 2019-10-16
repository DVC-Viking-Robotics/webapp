""" A collection of Flask routes """
# pylint: disable=invalid-name

import os
from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .sockets import socketio
from .users import User, DB

blueprint = Blueprint('blueprint', __name__)

@blueprint.route('/')
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """ Renders the register page """
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    user = User(username, generate_password_hash(password))
    if User.query.filter_by(username=username).count() > 0:
        flash("Account already exists", 'error')
    else:
        DB.session.add(user)
        DB.session.commit()
        flash('User successfully registered', 'success')
    return redirect('/login')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    If it's a POST request, it will attempt to log the user in.
    Otherwise, it renders the login page.
    """
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    registered_user = User.query.filter_by(username=username).first()
    if registered_user and check_password_hash(registered_user.password, password):
        login_user(registered_user)
        flash('Logged in successfully', 'success')
    else:
        flash('Username or Password is invalid', 'error')
        return redirect('/login')
    return redirect('home')


@blueprint.route('/logout')
@login_required
def logout():
    """ Redirects to login page after logging out """
    logout_user()
    return redirect('login')


@blueprint.route('/')
@blueprint.route('/home')
@login_required
def home():
    """ Renders the home page """
    return render_template('home.html', title='Home')


@blueprint.route('/remote')
@login_required
def remote():
    """ Renders the remote page """
    return render_template('remote.html', title='Remote Control')


@blueprint.route('/sensors')
@login_required
def sensors():
    """ Renders the sensor dashboard page """
    return render_template('sensors.html', title='Sensor Dashboard')


@blueprint.route('/automode')
@login_required
def automode():
    """ Renders the autonomous page """
    return render_template('automode.html', title='Autonomous Navigation')


@blueprint.route('/terminal')
@login_required
def terminal():
    """ Renders the virtual terminal page """
    return render_template('terminal.html', title='Terminal I/O')


@blueprint.route('/settings')
@login_required
def settings_page():
    """ Renders the settings page """
    return render_template('settings.html', title='Settings')


@blueprint.route('/about')
def about():
    """ Renders the about page """
    return render_template('about.html', title='About this project')


@blueprint.route("/shutdown_server")
@login_required
def shutdown_server():
    """ Shutdowns the webapp. """
    socketio.stop()


@blueprint.route("/restart")
@login_required
def restart():
    """ Restarts the robot (Only applicable if webserver runs off rasp pi) """
    os.system('sudo reboot')


@blueprint.route("/shutdown_robot")
@login_required
def shutdown_robot():
    """ Shutsdown the robot (Only applicable if webserver runs off rasp pi) """
    os.system('sudo shutdown -h now')


@blueprint.route("/delete_user")
@login_required
def delete_user():
    """ Deletes the current user's account. """
    DB.session.delete(current_user)
    DB.session.commit()
    flash("Account deleted", 'success')
    return redirect('/login')


@blueprint.route("/reset_password", methods=['GET', 'POST'])
@login_required
def reset_password():
    """ Resets the current user's password. """
    if request.method == 'GET':
        return render_template('home.html')

    old_password = request.form['old-password']
    new_password = request.form['new-password']
    user = current_user

    if check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password)
        DB.session.add(user)
        DB.session.commit()
        flash("Password has been updated", 'success')
    else:
        flash("Incorrect old password", 'error')

    return redirect('home.html')

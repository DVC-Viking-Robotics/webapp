# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, login_user, logout_user
from .users import users, User, db
from .sockets import socketio

blueprint = Blueprint('blueprint', __name__)

@blueprint.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('login.html')
    user = User(request.form['username'] , request.form['password'],)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect('/login')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page"""
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
      flash('Username or Password is invalid' , 'error')
      return redirect('/login')
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect('home')


@blueprint.route("/logout")
@login_required
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


@blueprint.route('/terminal')
@login_required
def terminal():
    return render_template('terminal.html', title='Terminal I/O')


@blueprint.route('/settings')
@login_required
def settings_page():
    return render_template('settings.html', title='Settings')


@blueprint.route('/about')
def about():
    return render_template('about.html', title='About this project')


@blueprint.route("/shutdown_server")
@login_required
def shutdown_server():
    """Shutdowns Webapp"""
    socketio.stop()
    return


@blueprint.route("/restart")
@login_required
def restart():
    """Restarts Robot (Only applicable if webserver runs off rasp pi)"""
    os.system('sudo reboot')
    return


@blueprint.route("/shutdown_robot")
@login_required
def shutdown_robot():
    """Shutsdown Robot (Only applicable if webserver runs off rasp pi)"""
    os.system('sudo shutdown -h now')
    return

# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from flask import Blueprint, render_template, request, flash, redirect, session
from flask_login import login_required, login_user, logout_user, current_user
from .users import User, db
from .sockets import socketio

blueprint = Blueprint('blueprint', __name__)


@blueprint.route('/')
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if User.query.filter_by(username=username).count() > 0:
        flash("Account already exists",'error')
        return redirect('/login')
    else:
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered','success')
    return redirect('/login')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page"""
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect('/login')
    login_user(registered_user)
    flash('Logged in successfully', 'success')
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


@blueprint.route("/delete_user")
@login_required
def delete_user():
    "Deletes users account"
    db.session.delete(current_user)
    db.session.commit()
    flash("Account deleted", 'success')
    return redirect('/login')


@blueprint.route("/reset_password", methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'GET':
        return render_template('home.html')
    old_password = request.form['old-password']
    new_password = request.form['new-password']
    user = current_user
    if User.query.filter_by(password=old_password).count() > 0:
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        flash("Password has been updated", 'success')
        return redirect('home')
    else:
        flash("Incorrect old password",'error')
        return redirect('home')
    return

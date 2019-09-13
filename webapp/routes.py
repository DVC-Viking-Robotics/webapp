# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

from flask import Blueprint, render_template

blueprint = Blueprint('blueprint', __name__)


@blueprint.route('/')
@blueprint.route('/remote')
def remote():
    """Renders the remote control page."""
    return render_template(
        'remote.html',
        title='Remote Control')

@blueprint.route('/extras')
def extras():
    """Renders the features page."""
    return render_template(
        'extras.html',
        title='Extra Features',
        message='Try our more advanced features!'
    )

@blueprint.route('/vidFeed')
def vidFeed():
    """Renders the camera page."""
    return render_template(
        'vidFeed.html',
        title='Live Camera feed',
        message='straight from the Robot!'
    )

@blueprint.route('/automode')
def automode():
    """Google maps API with coordinate selection for auto mode."""
    return render_template(
        'automode.html',
        title='Autonomous Navigation',
        message='Autonomous Nav Mode'
    )

@blueprint.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About this project:',
        message='This Web App is meant to control a robot powered by Raspberry Pi via WiFi or LAN. '
    )

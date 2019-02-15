"""
This script runs the flask_controller application using a development server.
"""

import os
from flask import Flask, g, render_template
import flask_sijax
# from outputs.drivetrain import drivetrain

# d = drivetrain(17, 27, 22, 23)
called = False
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/remote', methods=['GET', 'POST'])
def remote():
    """Renders the remote control page."""
    def robot(obj_response, x, y, z):
        #print("x: ", x, " y: ", y, " z: ", z)
        # d.go(x, y)
        print("function called successfully!")
        if g.sijax.is_sijax_request:
            obj_response.alert('function called successfully!')
            # Sijax request detected - let Sijax handle it
            g.sijax.register_callback('robot', robot)
            return g.sijax.process_request()

    return render_template(
        'remote.html',
        title='Remote Control')

@app.route('/extras')
def extras():
    """Renders the features page."""
    return render_template(
        'extras.html',
        title='Extra Features',
        message='Try our more advanced features!'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About this project:',
        message='This Web App is meant to control a robot powered by Raspberry Pi via WiFi hotspot. It uses various Python modules including Flask(web site server), HostAPD(hotspot), gpiozero(Robot and servo classes) and some custom written modules.'
    )

if __name__ == '__main__':
    app.run('0.0.0.0', 5555)


"""
This script runs the flask_controller application using a development server.
"""
from flask import Flask
from .pages_config import ALL_PAGES, NUM_ROWS
from .routes import blueprint
from .users import login_manager
from .sockets import socketio, cmd, d, nav, IMUsensor

# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.register_blueprint(blueprint)
login_manager.init_app(app)
socketio.init_app(app)

@app.context_processor
def inject_constants():
    return dict(
        ALL_PAGES=ALL_PAGES,
        NUM_ROWS=NUM_ROWS
    )

if __name__ == '__main__':
    try:
        socketio.run(app, host=cmd['WhoAmI']['host'], port=int(cmd['WhoAmI']['port']), debug=False)
    except KeyboardInterrupt:
        socketio.stop()
        if d is not None:
            d.go(0, 0)
        del d, nav, IMUsensor
    # finally:
    # d.go(0,0)
    #nav.alignHeading(0)
    # input("Press Enter to continue...")
    #nav.alignHeading(180)

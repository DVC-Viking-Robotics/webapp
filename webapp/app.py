"""
This script runs the flask_controller application using a development server.
"""
from flask import Flask
from flask_compress import Compress
from flask_cachebuster import CacheBuster
from datetime import timedelta
import click
from .pages_config import ALL_PAGES, NUM_ROWS
from .routes import blueprint
from .users import login_manager
from .sockets import socketio

compress = Compress()

cache_config = {
    'extensions': ['.js', '.css'],  # allowed extentions for caching
    'hash_size': 10                         # length of hash string
}

cache_buster = CacheBuster(config=cache_config)

# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring,no-value-for-parameter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.register_blueprint(blueprint)
login_manager.init_app(app)
socketio.init_app(app)

# Enable gzip compression of static assets
compress.init_app(app)

# Enable indefinite caching of static assets based on hash values
cache_buster.init_app(app)

# Cache all static files for 1 year by default
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=60 * 60 * 24 * 365)

@app.context_processor
def inject_constants():
    return dict(
        ALL_PAGES=ALL_PAGES,
        NUM_ROWS=NUM_ROWS
    )

@click.command()
@click.option('--port', default=5555, help='The port number used to access the webapp.')
def run(port):
    try:
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        socketio.stop()

if __name__ == '__main__':
    run()

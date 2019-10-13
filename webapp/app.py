"""
This script runs the flask_controller application using a development server.
"""
import click
import os
from flask import Flask
from .constants import TECH_USED, PAGES_CONFIG
from .config import DISABLE_AUTH_SYSTEM
from .routes import blueprint
from .sockets import socketio
from .users import login_manager
from .utils.static_optimizer import cache_buster, asset_compressor
from .utils.file_encryption import EncryptedFileManager

if not DISABLE_AUTH_SYSTEM:
    from .users import db

# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring,no-value-for-parameter

app = Flask(__name__)

app.secret_key = b'\x93:\xda\x0cf[\x8c\xc5\xb7D\xa8\xebH\x1d\x9e-7\xca\xe7\x1e\xea\xac\x15.'

# Cache all static files for 1 year by default
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60 * 60 * 24 * 365

if not DISABLE_AUTH_SYSTEM:
    # Read the encrypted database URI and re-encrypt it again
    SECRET_KEYFILE = 'secret/secret.key'
    DB_CONFIG_FILE = 'secret/db-config.encrypted'

    db_config_manager = EncryptedFileManager(SECRET_KEYFILE)
    URI = db_config_manager.read_file(DB_CONFIG_FILE).decode('utf-8')

    app.config['SQLALCHEMY_DATABASE_URI'] = URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

app.register_blueprint(blueprint)

# Enable login management
login_manager.init_app(app)

# Enable WebSocket integration
socketio.init_app(app)

# Enable gzip compression of static assets
asset_compressor.init_app(app)

# Enable indefinite caching of static assets based on hash values
cache_buster.init_app(app)


@app.context_processor
def inject_constants():
    return dict(
        ALL_PAGES=PAGES_CONFIG['ALL_PAGES'],
        NUM_ROWS=PAGES_CONFIG['NUM_ROWS'],
        OSS_SERVER_LIST=TECH_USED['OSS_SERVER_LIST'],
        OSS_CLIENT_LIST=TECH_USED['OSS_CLIENT_LIST'],
    )


@click.command()
@click.option('--port', default=5555, help='The port number used to access the webapp.')
def run(port):
    try:
        print(f'Hosting @ http://localhost:{port}')
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        socketio.stop()


if __name__ == '__main__':
    run()

"""
This script runs the flask_controller application using a development server.
"""
import click
from flask import Flask
from .pages_config import ALL_PAGES, NUM_ROWS
from .oss_lib_list import OSS_SERVER_LIST, OSS_CLIENT_LIST
from .routes import blueprint
from flask_sqlalchemy import SQLAlchemy
from .sockets import socketio
from .static_optimizer import cache_buster, compress
from .users import login_manager
# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring,no-value-for-parameter

app = Flask(__name__)

app.secret_key = b'\x93:\xda\x0cf[\x8c\xc5\xb7D\xa8\xebH\x1d\x9e-7\xca\xe7\x1e\xea\xac\x15.'
# Cache all static files for 1 year by default
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60 * 60 * 24 * 365
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://UserAdmin:^0o9JpRAPazf@webapp-dev-db.c1cjueiaoepn.us-west-1.rds.amazonaws.com:3306/user.accounts'

db = SQLAlchemy()

app.register_blueprint(blueprint)

db.init_app(app)

# Enable login management
login_manager.init_app(app)

# Enable WebSocket integration
socketio.init_app(app)

# Enable gzip compression of static assets
compress.init_app(app)

# Enable indefinite caching of static assets based on hash values
cache_buster.init_app(app)


@app.context_processor
def inject_constants():
    return dict(
        ALL_PAGES=ALL_PAGES,
        NUM_ROWS=NUM_ROWS,
        OSS_SERVER_LIST=OSS_SERVER_LIST,
        OSS_CLIENT_LIST=OSS_CLIENT_LIST,
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

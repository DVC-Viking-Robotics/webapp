"""
A collection of constants that's used throughout the web app.
"""

import os
import json
from .utils.file_encryption import FernetVault

# NOTE: When sphinx generates the docs automatically, it will try to import the file relative
# to where the build command was issues, which means that the string path isn't guaranteed
# to refer to the same file location. Thus, we use this file as a basis for figuring out the
# root location of the web app and access whichever files are needed from there.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
TECH_USED_FILE = os.path.join(ROOT_DIR, 'webapp/constants/technology-used.json')
PAGES_CONFIG_FILE = os.path.join(ROOT_DIR, 'webapp/constants/pages-config.json')

# Prepare constants from JSON files
with open(TECH_USED_FILE, 'r') as fp:
    TECH_USED = json.load(fp)
    """A exhaustive list of all the technology used for this project."""

with open(PAGES_CONFIG_FILE, 'r') as fp:
    PAGES_CONFIG = json.load(fp)
    """A front-end configuration for the arrangement of the page tiles for the home page."""

ONE_YEAR = 60 * 60 * 24 * 365
"""The time of one year in seconds."""

SECRET_KEYFILE = os.path.join(ROOT_DIR, 'secret/secret.key')
"""Location of master secret keyfile for DB URI and Flask secret encryption."""

DB_CONFIG_FILE = os.path.join(ROOT_DIR, 'secret/db-config.encrypted')
"""Location of encrypted DB URI file."""

FLASK_SECRET_FILE = os.path.join(ROOT_DIR, 'secret/flask-secret.encrypted')
"""Location of encrypted flask secret file."""

# pylint: disable=invalid-name

# Read and decrypt the encrypted database URI and Flask secret
# NOTE: If RTD is executing this file, it will never find the secret key as it's gitignored
if not os.getenv('READTHEDOCS', None):
    vault = FernetVault(SECRET_KEYFILE)
    DB_URI = vault.read_file(DB_CONFIG_FILE).decode('utf-8')
    """The database URI for facilitating user management."""

    FLASK_SECRET = vault.read_file(FLASK_SECRET_FILE)
    """Used by Flask to securely sign cookies."""
else:
    DB_URI = 'sqlite://'
    FLASK_SECRET = os.urandom(24)

LOCAL_DB_URI = 'sqlite:///../users.db'
"""Database URI used when using local database. See `config.LOCAL_DATABASE` for more info."""

STATIC_CACHE_CONFIG = {
    'extensions': ['.js', '.css'],  # enabled extentions for caching
    'hash_size': 10                 # length of hash string
}
"""Configuration for cache busting common static files."""

"""
A collection of constants that's used throughout the web app.
"""

import os
import json
from .utils.file_encryption import FernetVault

# Restricts variables exposed via a wildcard import
__all__ = [
    'TECH_USED', 'PAGES_CONFIG', 'ONE_YEAR',
    'SECRET_KEYFILE', 'DB_CONFIG_FILE', 'FLASK_SECRET_FILE',
    'DB_URI', 'FLASK_SECRET', 'STATIC_CACHE_CONFIG'
]

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

with open(PAGES_CONFIG_FILE, 'r') as fp:
    PAGES_CONFIG = json.load(fp)

ONE_YEAR = 60 * 60 * 24 * 365

SECRET_KEYFILE = os.path.join(ROOT_DIR, 'secret/secret.key')
DB_CONFIG_FILE = os.path.join(ROOT_DIR, 'secret/db-config.encrypted')
FLASK_SECRET_FILE = os.path.join(ROOT_DIR, 'secret/flask-secret.encrypted')

# pylint: disable=invalid-name

# Read and decrypt the encrypted database URI and Flask secret
vault = FernetVault(SECRET_KEYFILE)
DB_URI = vault.read_file(DB_CONFIG_FILE).decode('utf-8')
FLASK_SECRET = vault.read_file(FLASK_SECRET_FILE)

STATIC_CACHE_CONFIG = {
    'extensions': ['.js', '.css'],  # enabled extentions for caching
    'hash_size': 10                 # length of hash string
}

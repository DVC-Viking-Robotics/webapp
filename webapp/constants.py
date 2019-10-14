"""
A collection of constants that's used throughout the web app.
"""

import json
from .utils.file_encryption import FernetVault

# Restricts variables exposed via a wildcard import
__all__ = [
    'TECH_USED', 'PAGES_CONFIG', 'ONE_YEAR',
    'SECRET_KEYFILE', 'DB_CONFIG_FILE', 'FLASK_SECRET_FILE',
    'DB_URI', 'FLASK_SECRET'
]

# Prepare constants from JSON files
with open('webapp/constants/technology-used.json', 'r') as fp:
    TECH_USED = json.load(fp)

with open('webapp/constants/pages-config.json', 'r') as fp:
    PAGES_CONFIG = json.load(fp)

ONE_YEAR = 60 * 60 * 24 * 365

SECRET_KEYFILE = 'secret/secret.key'
DB_CONFIG_FILE = 'secret/db-config.encrypted'
FLASK_SECRET_FILE = 'secret/flask-secret.encrypted'

# pylint: disable=invalid-name

# Read and decrypt the encrypted database URI and Flask secret
vault = FernetVault(SECRET_KEYFILE)
DB_URI = vault.read_file(DB_CONFIG_FILE).decode('utf-8')
FLASK_SECRET = vault.read_file(FLASK_SECRET_FILE)

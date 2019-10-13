import json

# Restricts variables exposed via a wildcard import
__all__ = ['TECH_USED', 'PAGES_CONFIG', 'SECRET_KEYFILE', 'DB_CONFIG_FILE', 'FLASK_SECRET_KEY']

# Prepare constants from JSON files
with open('webapp/constants/technology-used.json', 'r') as fp:
    TECH_USED = json.load(fp)

with open('webapp/constants/pages-config.json', 'r') as fp:
    PAGES_CONFIG = json.load(fp)

SECRET_KEYFILE = 'secret/secret.key'
DB_CONFIG_FILE = 'secret/db-config.encrypted'
FLASK_SECRET_FILE = 'secret/flask-secret.encrypted'

FLASK_SECRET_KEY = b'\x93:\xda\x0cf[\x8c\xc5\xb7D\xa8\xebH\x1d\x9e-7\xca\xe7\x1e\xea\xac\x15.'
"""
This script allows the admin to generate a new Fernet key file and re-encrypt
any '.encrypted' file, should the old key file be compromised.

Run it with ``python -m tools.gen_flask_secret``
"""

import os
from webapp.utils.file_encryption import FernetVault
from webapp.constants import SECRET_KEYFILE, FLASK_SECRET_FILE
from webapp.utils.super_logger import logger

if __name__ == '__main__':
    if not os.path.exists(SECRET_KEYFILE):
        logger.info('Tools', 'Error: You must have the original key file before you can change to a new one.')
        exit(-1)

    # generate new Flask secret key save it
    vault = FernetVault(SECRET_KEYFILE)
    NEW_FLASK_SECRET = os.urandom(24)
    vault.write_file(NEW_FLASK_SECRET, FLASK_SECRET_FILE)

"""
This script allows the admin to generate a new secret key, should the old one be compromised.

Run it with ``python -m tools.decrypt_contents``
"""

import os
from webapp.utils.file_encryption import FernetVault
from webapp.constants import SECRET_KEYFILE, DB_CONFIG_FILE, FLASK_SECRET_FILE
from webapp.utils.super_logger import logger

if __name__ == '__main__':
    if not os.path.exists(SECRET_KEYFILE):
        logger.error('Tools', 'Error: You must have the original key file to decrypt the encrypted contents.')
        exit(-1)

    # read URI and Flask secret with key file
    vault = FernetVault(SECRET_KEYFILE)
    DB_URI = vault.read_file(DB_CONFIG_FILE)
    FLASK_SECRET = vault.read_file(FLASK_SECRET_FILE)

    logger.info('Tools', f'Database URI: {DB_URI}')
    logger.info('Tools', f'Flask Secret Key: {FLASK_SECRET}')

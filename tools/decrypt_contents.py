"""
This script allows the admin to generate a new secret key, should the old one be compromised.

Run it with ``python -m tools.decrypt_contents``
"""

import os
from webapp.utils.file_encryption import FernetVault
from webapp.constants import SECRET_KEYFILE, DB_CONFIG_FILE, FLASK_SECRET_FILE

# pylint: disable=invalid-name

if __name__ == '__main__':
    if not os.path.exists(SECRET_KEYFILE):
        print("Error: You must have the original key file to decrypt the encrypted contents.")
        exit(-1)

    # read URI and Flask secret with key file
    vault = FernetVault(SECRET_KEYFILE)
    DB_URI = vault.read_file(DB_CONFIG_FILE)
    FLASK_SECRET = vault.read_file(FLASK_SECRET_FILE)

    print(f'Database URI:      {DB_URI}')
    print(f'Flask Secret Key:  {FLASK_SECRET}')

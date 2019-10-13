import os
from cryptography.fernet import Fernet
from webapp.utils.file_encryption import FernetVault
from webapp.constants import SECRET_KEYFILE, DB_CONFIG_FILE, FLASK_SECRET_FILE

"""
This script allows the admin to generate a new secret key, should the old one be compromised.
"""
if __name__ == '__main__':
    if not os.path.exists(SECRET_KEYFILE):
        print("Error: You must have the original key file to decrypt the encrypted contents.")
        exit(-1)

    # read URI and Flask secret with key file
    vault = FernetVault(SECRET_KEYFILE)
    URI = vault.read_file(DB_CONFIG_FILE)
    FLASK_SECRET = vault.read_file(FLASK_SECRET_FILE)

    print(f'Database URI:      {URI}')
    print(f'Flask Secret Key:  {FLASK_SECRET}')
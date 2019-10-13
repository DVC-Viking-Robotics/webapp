import os
from cryptography.fernet import Fernet
from webapp.utils.file_encryption import FernetVault
from webapp.constants import SECRET_KEYFILE, FLASK_SECRET_FILE

"""
This script allows the admin to generate a new Fernet key file and re-encrypt
any '.encrypted' file, should the old key file be compromised.
"""
if __name__ == '__main__':
    if not os.path.exists(SECRET_KEYFILE):
        print("Error: You must have the original key file before you can change to a new one.")
        exit(-1)

    # generate new Flask secret key save it
    vault = FernetVault(SECRET_KEYFILE)
    NEW_FLASK_SECRET = os.urandom(24)
    vault.write_file(NEW_FLASK_SECRET, FLASK_SECRET_FILE)
"""
This module allows easy encryption/decryption of files via Fernet cryptography
"""

from cryptography.fernet import Fernet

# pylint: disable=invalid-name

class FernetVault:
    """ A file vault that decrypts the contents of an encrypted file given a key file. """

    def __init__(self, key_file_path):
        """ Initialize the vault with a master key file. """
        with open(key_file_path, 'rb') as fp:
            self.key = fp.read()

    def read_file(self, input_file):
        """ Read an encrypted file. """
        with open(input_file, 'rb') as fp:
            data = fp.read()
            fernet = Fernet(self.key)
            decrypted = fernet.decrypt(data)
            return decrypted

    def write_file(self, data, output_file):
        """ Write an encrypted file. """
        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as fp:
            fp.write(encrypted)

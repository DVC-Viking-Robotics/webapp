from cryptography.fernet import Fernet

class EncryptedFileManager:
    def __init__(self, key_file_path):
        with open(key_file_path, 'rb') as fp:
            self.key = fp.read()

    def read_file(self, input_file):
        with open(input_file, 'rb') as fp:
            data = fp.read()
            fernet = Fernet(self.key)
            decrypted = fernet.decrypt(data)
            return decrypted

    def write_file(self, data, output_file):
        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as fp:
            fp.write(encrypted)
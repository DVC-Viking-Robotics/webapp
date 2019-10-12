from cryptography.fernet import Fernet
import os

file = open('key.key', 'rb')
key = file.read() # The key will be type bytes
file.close()
def encrypt_file(input_file):
    output_file = "webapp/output.encrypted"

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    os.remove(input_file)

def decrypt_file():
    from cryptography.fernet import Fernet
    input_file = 'webapp/output.encrypted'
    output_file = 'webapp/server_config.txt'

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    os.remove(input_file)

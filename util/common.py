import sys
from string import Template
import getpass
import pyaes
from hashlib import sha256
import re

MAX_MSG_LENGTH = 30


def user_inf():
    player = sys.argv[0].split('.', 1)[0]
    BUFFER_DIR = Template('/tmp/$usr/').substitute(usr=getpass.getuser())
    BUFFER_FILE_NAME = 'buffer'
    return player, BUFFER_DIR, BUFFER_FILE_NAME


def pad(msg, length):
    return bytes(str(msg).ljust(length), 'ascii')


def password_checker(password):
    return all(re.search(pattern, password) for pattern in
               ('.{5}', '[A-Z]', '\d.*\d', '^[^Ee]*$', '[!@#$%^&]'))


class AES:
    def __init__(self, key):
        self.key = sha256(bytes(str(key), 'ascii')).digest()
        self.encrypt_counter = 0
        self.decrypt_counter = 0

    def encrypt(self, plaintext):
        counter = pyaes.Counter(initial_value=self.encrypt_counter)
        aes = pyaes.AESModeOfOperationCTR(self.key, counter=counter)
        self.encrypt_counter += len(plaintext)
        return aes.encrypt(plaintext)

    def decrypt(self, ciphertext):
        counter = pyaes.Counter(initial_value=self.decrypt_counter)
        aes = pyaes.AESModeOfOperationCTR(self.key, counter=counter)
        self.decrypt_counter += len(ciphertext)
        return aes.decrypt(ciphertext)

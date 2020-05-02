import socket
from util.common import *
from util.pyDH import *
from util.dialog import *

player, BUFFER_DIR, BUFFER_FILE_NAME = user_inf()
buffer_path = BUFFER_DIR + BUFFER_FILE_NAME
_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
_socket.connect(buffer_path)

d1 = DiffieHellman()

local_key = d1.gen_public_key()
bank_public_key = int(_socket.recv(2048).decode())
_socket.sendall(pad(local_key, 2048))
shared = d1.gen_shared_key(bank_public_key)

aes = AES(shared)
dialog = Dialog('print')

dialog.welcome('welcome to our bank application')
dialog.chat(shared + '\n')
dialog.info("Are you a new user (y,n)")

answer = input()

if answer in ('y', 'Y', 'yes', 'Yes'):
    _socket.sendall('1'.encode())
    Username = input("Enter username: ")
    Password = input("Enter password: ")

    while not password_checker(Password):
        dialog.prompt('Passwords must be at least 5 characters,upper case letter,\n'
                      'least two numbers,least one special symbol\n ')
        Password = input("Enter password: ")

    _socket.sendall(aes.decrypt(Username))
    _socket.sendall(aes.decrypt(Password))


elif answer in ('n', 'N', 'No', 'no'):
    _socket.sendall('0'.encode())

    Username = input("Enter username: ")
    Password = input("Enter password: ")

    _socket.sendall(aes.decrypt(Username))
    _socket.sendall(aes.decrypt(Password))

    if _socket.recv(8).decode() == 'pass':
        dialog.chat('Congratulations you have won a million dollars')
    else:
        dialog.prompt('access denied')
else:
    dialog.prompt('error')

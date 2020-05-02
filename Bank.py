import socket
from util.common import *
import os, errno
from util.pyDH import *
from util.dialog import *
from util.database import *

player, BUFFER_DIR, BUFFER_FILE_NAME = user_inf()
_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
buffer_path = BUFFER_DIR + BUFFER_FILE_NAME

try:
    os.makedirs(BUFFER_DIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

_socket.bind(buffer_path)
_socket.listen(1)
conn, rem_addr = _socket.accept()

d1 = DiffieHellman()

local = d1.gen_public_key()
conn.sendall(pad(local, 2048))
l1 = int(conn.recv(2048).decode())
shared = d1.gen_shared_key(l1)

aes = AES(shared)
dialog = Dialog('print')
dialog.chat(shared)

answer = conn.recv(2).decode()
Username = aes.encrypt(conn.recv(1024)).decode()
Password = aes.encrypt(conn.recv(1024)).decode()

if answer == '1':
    add_user(Username, Password)
else:
    if user_validation(Username, Password):
        conn.sendall('pass'.encode())
    else:
        conn.sendall('access denied'.encode())

print(Username, Password)

conn.close()
os.remove(BUFFER_DIR + BUFFER_FILE_NAME)

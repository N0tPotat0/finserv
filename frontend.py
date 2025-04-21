import socket
import os
import time

HOST = '192.168.1.4'
PORT = 5050
BUFFER_SIZE = 4096
FILE_PATH = "C:\\users\\kirill\\downloads\\textadder.vbs"
#FILE_PATH = "C:\\users\\kirill\\downloads\\test123.txt"
tokenPath = "C:\\users\\kirill\\downloads\\testtoken.txt"

with open(tokenPath, 'rb') as f:
    token = f.read()
    token = token[:]
    print(token)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect ((HOST, PORT))

    if s.recv(BUFFER_SIZE).decode() == "ACCESS TOKEN":
        s.send(token)
        print("ACCESS TOKEN REQ RECEIVED")

    if s.recv(BUFFER_SIZE).decode() == "CORRECT TOKEN":
        print("Token handshake passed")

    filename = os.path.basename(FILE_PATH)
    print(filename)
    s.send(filename.encode())

    ack = s.recv(BUFFER_SIZE).decode()
    while ack != "READY":
        print("[X] Server not ready")
        time.sleep(1)

    with open(FILE_PATH, 'rb') as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)

    print(f"File {filename} sent successfullly")

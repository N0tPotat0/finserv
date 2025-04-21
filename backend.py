import socket
import os
import time

with open("testtoken.txt") as f:
    token = f.read()

tokeninvalid = True
    
HOST = '0.0.0.0'
PORT = 5050
BUFFER_SIZE = 4096

cwd = os.getcwd()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server listening on {HOST}:{PORT}...")

try:
    conn, addr = server.accept()
    print(f"[+] Connected by {addr}")
    while tokeninvalid:
        conn.send(b"ACCESS TOKEN")
        received = conn.recv(BUFFER_SIZE).decode()
        if received == token:
            tokeninvalid = False
        else: print("Waiting for valid token")

    conn.send(b"CORRECT TOKEN")
    print("Correct token received, downloading")

    filename = conn.recv(BUFFER_SIZE).decode()
    print(f"[>] Receiving file: {filename}")

    conn.send(b"READY")
    

    with open(filename, 'wb') as f:
        while True:
            bytes_read = conn.recv(BUFFER_SIZE)
            print("writing......................")
            if not bytes_read:
                break
            f.write(bytes_read)

except Exception as e:
    print(f"[!] Error: {e}")

finally:
    conn.close()
    server.close()

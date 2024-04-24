import socket
import threading
import os
import sys


def handle(conn,dir):
    while True:
        data = conn.recv(2048).decode()
        if data:
            data = data.split("\r\n")
            method, path, version = data[0].split(" ")

            if path == '/':
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            elif path.startswith("/echo/"):
                text = path.split("/echo/")[-1]
                output = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}\r\n"
                conn.sendall(output.encode())
            elif path == "/user-agent":
                text = data[2].split("User-Agent: ")[-1]
                output = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}\r\n"
                conn.sendall(output.encode())

            elif path.startswith("/files/"):
                filename = path.split("/files/")[-1]
                file_path = dir + "/" + filename
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        data = f.read()
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(data)}\r\n\r\n"
                        conn.sendall(response.encode())
                        conn.sendall(data)
                else:
                    conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            else:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, addr = server_socket.accept()  # wait for client
        dire = None
        if len(sys.argv) > 1:
            dire = sys.argv[2]
        client_handler = threading.Thread(target=handle, args=(conn, dire))
        client_handler.start()



if __name__ == "__main__":
    main()

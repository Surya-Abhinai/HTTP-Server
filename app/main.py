import socket
import threading
import os
import sys

def handle_client(client_socket, dir):
    while True:
        data = client_socket.recv(4096).decode()
        if not data:
            break
        data_list = data.split("\r\n")
        path = data_list[0].split(" ")[1]
        if str(path) == "/":
            client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
        elif "/echo/" in str(path):
            msg = path.split("/echo/")[-1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}"
            client_socket.sendall(response.encode())
        elif str(path) == "/user-agent":
            user_info = data_list[2].split(" ")[-1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_info)}\r\n\r\n{user_info}"
            client_socket.sendall(response.encode())
        elif "/files/" in str(path):
            filename = path.split("/files/")[-1]
            file_path = dir + "/" + filename
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    data = f.read()
                    contentLength = len(data)
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {contentLength}\r\n\r\n"
                    client_socket.sendall(response.encode())
                    client_socket.sendall(data)
            else:
                client_socket.sendall(
                    b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                )
        else:
            client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            client_socket.sendall(
                b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
            )
    client_socket.close()
def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    while True:
        client_socket, _ = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        if len(sys.argv) > 1:
            dir = sys.argv[2]
            client_handler = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    dir,
                ),
            )
        else:
            client_handler = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    None,
                ),
            )
        client_handler.start()
if __name__ == "__main__":
    main()
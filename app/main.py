import socket
import re

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    pattern = r'/echo/(.*)'
    echo = re.compile(pattern)
    while True:
        data = conn.recv(2048).decode()
        if data:
            data = data.split("\r\n")
            method,path,version = data[0].split(" ")
            match = re.search(path)
            if path == '/':
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            elif match:
                text = match.group(1)
                output = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n{text}\r\n"
                conn.sendall(output.encode())
            else:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")


if __name__ == "__main__":
    main()

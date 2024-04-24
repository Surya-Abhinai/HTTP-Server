import socket
import re

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    # pattern = r'/echo/(.*)'
    # echo = re.compile(pattern)
    while True:
        data = conn.recv(2048).decode()
        if data:
            data = data.split("\r\n")
            method,path,version = data[0].split(" ")
            # match = echo.search(path)
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
            else:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")


if __name__ == "__main__":
    main()

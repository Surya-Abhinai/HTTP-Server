import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    while True:
        data = conn.recv(2048).decode()
        if data:
            data = data.split("\r\n")
            method , path , version = data[0].split(" ")

            if path == '/':
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")


if __name__ == "__main__":
    main()

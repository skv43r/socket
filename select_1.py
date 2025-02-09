import socket
from select import select

to_check = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f"Connetion from: {addr}")
    to_check.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        response = f"Server received: {request.decode('utf-8')}".encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        readable, writable, errored = select(to_check, [], [])

        for socket in readable:
            if socket == server_socket:
                accept_connection(socket)
            else:
                send_message(socket)


if __name__ == "__main__":
    to_check.append(server_socket)
    event_loop()
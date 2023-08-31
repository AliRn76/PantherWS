import socket

from wsproto import ConnectionType, WSConnection
from wsproto.events import (
    AcceptConnection,
    CloseConnection,
    Message,
    Ping,
    Request,
    TextMessage,
)

MAX_CONNECTS = 5
RECEIVE_BYTES = 4096


def handle_connection(stream: socket.socket) -> None:
    """
    Handle a connection.

    The server operates a request/response cycle, so it performs a synchronous
    loop:

    1) Read data from network into wsproto
    2) Get new events and handle them
    3) Send data from wsproto to network

    :param stream: a socket stream
    """
    ws = WSConnection(ConnectionType.SERVER)
    running = True

    while running:
        # 1) Read data from network
        in_data = stream.recv(RECEIVE_BYTES)
        print("Received {} bytes".format(len(in_data)))
        ws.receive_data(in_data)

        # 2) Get new events and handle them
        out_data = b""
        for event in ws.events():
            if isinstance(event, Request):
                print("Accepting WebSocket upgrade")
                out_data += ws.send(AcceptConnection())
            elif isinstance(event, CloseConnection):
                print(
                    "Connection closed: code={} reason={}".format(
                        event.code, event.reason
                    )
                )
                out_data += ws.send(event.response())
                running = False
            elif isinstance(event, TextMessage):
                # Reverse text and send it back to wsproto
                print("Received request and sending response")
                out_data += ws.send(Message(data=event.data[::-1]))
            elif isinstance(event, Ping):
                print("Received ping and sending pong")
                out_data += ws.send(event.response())
            else:
                print(f"Unknown event: {event!r}")

        # 3) Send data from wsproto to network
        print("Sending {} bytes".format(len(out_data)))
        stream.send(out_data)


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen(0)

    try:
        while True:
            print("Waiting for connection...")
            (stream, addr) = server.accept()
            print("Client connected: {}:{}".format(addr[0], addr[1]))
            handle_connection(stream)
            stream.shutdown(socket.SHUT_WR)
            stream.close()
    except KeyboardInterrupt:
        print("Shutting down...")

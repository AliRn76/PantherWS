import socket

from wsproto import WSConnection
from wsproto.connection import ConnectionType
from wsproto.events import (
    AcceptConnection,
    CloseConnection,
    Message,
    Ping,
    Pong,
    Request,
    TextMessage,
)

RECEIVE_BYTES = 4096


def wsproto_demo(host: str, port: int) -> None:
    """
    Demonstrate wsproto:

    0) Open TCP connection
    1) Negotiate WebSocket opening handshake
    2) Send a message and display response
    3) Send ping and display pong
    4) Negotiate WebSocket closing handshake
    """

    # 0) Open TCP connection
    print(f"Connecting to {host}:{port}")
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))

    # 1) Negotiate WebSocket opening handshake
    print("Opening WebSocket")
    ws = WSConnection(ConnectionType.CLIENT)
    net_send(ws.send(Request(host=host, target="server")), conn)
    net_recv(ws, conn)
    handle_events(ws)

    # 2) Send a message and display response
    message = "wsproto is great"
    print(f"Sending message: {message}")
    net_send(ws.send(Message(data=message)), conn)
    net_recv(ws, conn)
    handle_events(ws)

    # 3) Send ping and display pong
    print(f"Sending ping")
    net_send(ws.send(Ping()), conn)
    net_recv(ws, conn)
    handle_events(ws)

    # 4) Negotiate WebSocket closing handshake
    print("Closing WebSocket")
    net_send(ws.send(CloseConnection(code=1000, reason="sample reason")), conn)
    net_recv(ws, conn)
    conn.shutdown(socket.SHUT_WR)
    net_recv(ws, conn)


def net_send(out_data: bytes, conn: socket.socket) -> None:
    print("Sending {} bytes".format(len(out_data)))
    conn.send(out_data)


def net_recv(ws: WSConnection, conn: socket.socket) -> None:
    in_data = conn.recv(RECEIVE_BYTES)
    if not in_data:
        print("Received 0 bytes (connection closed)")
        ws.receive_data(None)
    else:
        print("Received {} bytes".format(len(in_data)))
        ws.receive_data(in_data)


def handle_events(ws: WSConnection) -> None:
    for event in ws.events():
        if isinstance(event, AcceptConnection):
            print("WebSocket negotiation complete")
        elif isinstance(event, TextMessage):
            print(f"Received message: {event.data}")
        elif isinstance(event, Pong):
            print(f"Received pong: {event.payload!r}")
        else:
            raise Exception("Do not know how to handle event: " + str(event))


if __name__ == "__main__":
    wsproto_demo('127.0.0.1', 8000)

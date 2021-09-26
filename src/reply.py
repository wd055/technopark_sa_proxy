import socket
import ssl

from http_parser.pyparser import HttpParser

from src import consts


def receive_data_from_socket(sock):
    parser = HttpParser()
    resp = b''
    while True:
        data = sock.recv(consts.BUF_SIZE)
        if not data:
            break

        received = len(data)
        _ = parser.execute(data, received)
        resp += data

        if parser.is_message_complete():
            break
    return resp, parser


def send_http_request(request, host, port):
    req_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    req_socket.connect((host.strip(), port))
    req_socket.sendall(request.encode("utf-8"))
    return req_socket


def send_https_request(request: str, host: str, port: int = 443) -> socket.socket:
    req_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    req_socket.connect((host, port))
    ssl_req_socket = ssl.wrap_socket(req_socket)
    ssl_req_socket.send(request.encode())
    return ssl_req_socket


def get_reply_from_host(request: str, host: str, port: int, tls: int) -> bytes:
    if tls == 1:
        req_socket = send_https_request(request, host, port)
    else:
        req_socket = send_http_request(request, host, port)
    reply, _ = receive_data_from_socket(req_socket)

    req_socket.close()
    return reply

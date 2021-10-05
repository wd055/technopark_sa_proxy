
import socket

from http_parser.pyparser import HttpParser

from src import consts
from src.reply import get_reply_from_host


def build_http_request_to_host(parser: HttpParser, data: bytes):
    data_array = data.decode("utf-8").split("\n")
    url = ""

    if parser.is_headers_complete():
        url = parser.get_url()

    data_array[0] = data_array[0].replace(url, parser.get_path())
    host = parser.get_headers()['host']

    request_to_host = ""
    for line in data_array:
        if line.find("Proxy-Connection") >= 0:
            continue
        request_to_host += line + "\n"

    return request_to_host, host


def proxy_http(data: bytes, parser: HttpParser, con: socket.socket) -> bytes:
    request, host = build_http_request_to_host(parser, data)
    reply = get_reply_from_host(request, host, 80, 0)
    con.sendall(reply)
    con.close()
    consts.REP.insert_request(request, host, 0)
    return reply

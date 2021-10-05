from DB.DB import RequestDataBase
from _thread import start_new_thread
from repository import *
import socket

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


from src import consts
from src.proxy_http import proxy_http
from proxy_https import proxy_https


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


rep = RequestDataBase()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((consts.HOST, consts.PORT))
    sock.listen(5)

    while True:
        try:
            con, _ = sock.accept()
            data, parser = receive_data_from_socket(con)

            if parser.get_method() == "CONNECT":
                start_new_thread(
                    proxy_https, (con, parser.get_headers()['host'], 443))
            else:
                start_new_thread(proxy_http, (data, parser, con))

        except KeyboardInterrupt:
            sock.close()
            exit()

        except Exception as e:
            sock.close()
            print(e.args)
            exit()


if __name__ == '__main__':
    main()

import socket
from _thread import start_new_thread

from src import consts
from src.proxy_http import proxy_http
from src.proxy_https import proxy_https
from src.reply import receive_data_from_socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((consts.HOST, consts.PORT))
    sock.listen(5)

    while True:
        try:
            con, addr = sock.accept()
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

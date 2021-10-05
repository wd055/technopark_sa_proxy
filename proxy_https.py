import os
import socket
import ssl
import time
from random import random
from string import Template
from subprocess import PIPE, Popen, call

from src import consts
from src.reply import get_reply_from_host, receive_data_from_socket


def generate_cert(host: str):
    path = f'certs/{host}.crt'
    print(path)
    if not os.path.exists('certs'):
        os.makedirs('certs')
    if not os.path.exists(path):
        with open(path, 'w') as f:
            call(['./gen_cert.sh', host, str(int(random() * 1000000000))], stdout=f)
        print(f'Certificate to {host} generated')
    return path
    
# def generate_certificate(host, cert_path, conf_path):
#     epoch = "%d" % (time.time() * 1000)
#     p1 = Popen(["openssl", "req", "-new", "-key", consts.CERT_KEY, "-subj", "/CN=%s" % host,
#                 # "-addext", "subjectAltName = DNS:" + host
#                 ],
#                stdout=PIPE)
#     p2 = Popen(
#         ["openssl", "x509", "-req", "-extfile", conf_path, "-days", "3650", "-CA", consts.CA_CERT, "-CAkey", consts.CA_KEY,
#          "-set_serial", epoch,
#          "-out", cert_path], stdin=p1.stdout, stderr=PIPE)
#     p2.communicate()


connection_established_msg = b'HTTP/1.1 200 Connection Established\r\n\r\n'


# def generate_subj_altname_config(host) -> str:
#     conf_template = Template("subjectAltName=DNS:${hostname}")
#     conf_path = "%s/%s.cnf" % (consts.CERT_DIR.rstrip('/'), host)
#     with open(conf_path, 'w') as fp:
#         fp.write(conf_template.substitute(hostname=host))
#     return conf_path


def proxy_https(client_conn: socket.socket, host: str, port: int = 443):
    host = host.split(":")[0].strip()

    cert_path = "%s/%s.crt" % (consts.CERT_DIR.rstrip('/'), host)
    # conf_path = generate_subj_altname_config(host)
    # generate_certificate(host, cert_path, conf_path)
    conf_path = generate_cert(host)
    os.unlink(conf_path)

    client_conn.sendall(connection_established_msg)
    client_conn_secure = ssl.wrap_socket(
        client_conn, keyfile=consts.CERT_KEY, certfile=cert_path, server_side=True)
    client_conn_secure.do_handshake()

    request, _ = receive_data_from_socket(client_conn_secure)
    reply = get_reply_from_host(request.decode(), host, port, 1)

    client_conn_secure.sendall(reply)
    client_conn_secure.close()

    consts.REP.insert_request(request.decode(), host, 1)

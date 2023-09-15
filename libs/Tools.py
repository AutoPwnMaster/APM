from socket import socket, AF_INET, SOCK_DGRAM


def get_ipv4():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

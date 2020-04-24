import socket


def join_blocks(blocks):
    """
    Receives a list of bytelike blocks and joins them.
    :param blocks: A list of bytelike blocks
    :return: A bytearray containing all the bytes from the blocks, in the order they were provided.
    """
    return bytearray(b''.join(blocks))


def split_blocks(message, block_size):
    """
    Divides a message in blocks of size block_size. If the length of the message is not multiple of block_size,
    the last message will be shorter.
    :param message: byte-like message
    :param block_size: block size
    :return: an array with bytearrays of length block_size
    """
    return [bytearray(message[i:i + block_size]) for i in range(0, len(message), block_size)]


def create_socket(server):
    """
    Starts a connection to the server
    :param server: tuple of address and port
    :return: an open socket
    """
    # Connect to external server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server)
    return sock


def send_message(sock, message):
    """
    Sends a message to a server and returns the response
    :param sock: a socket.
    :param message: a string with the message.
    :return: response.
    """
    if message == "":
        return ""
    sock.sendall(message.encode())
    # Receive message from outgoing server
    fd = sock.makefile(errors="ignore")
    resp = fd.readline().strip()
    return resp

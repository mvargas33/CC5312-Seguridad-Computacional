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
    :return: an input socket and an output file
    """
    # Connect to external server
    sock_input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_input.connect(server)
    sock_output = sock_input.makefile(errors="ignore")
    return sock_input, sock_output


def send_message(input, output, message):
    """
    Sends a message to a server and returns the response
    :param sock: a socket.
    :param message: a string with the message.
    :return: sock_input: a socket to send messages.
    :return: sock_output: a file used to read messages.
    """
    if message == "":
        return ""
    input.sendall(message.encode())
    # Receive message from outgoing server
    resp = output.readline().strip()
    return resp


def hex_to_bytes(hexmsg):
    """
    Transforms a hex string to a bytearray.
    :param hexmsg: a hex string
    :return: a bytearray
    """
    return bytearray.fromhex(hexmsg)


def bytes_to_hex(bytearr):
    """
    Transforms a bytearray to a hex string.
    :param bytearr: a bytarray
    :return: a hex string
    """
    return bytearr.hex()
import socket

# We connect to a (host,port) tuple
import utils

CONNECTION_ADDR = ("cc5312.xor.cl", 5312)

if __name__ == "__main__":
    sock = utils.create_socket(CONNECTION_ADDR)
    while True:
        try:

            # Read a message from standard input
            response = input("send a message: ")
            # You need to use encode() method to send a string as bytes.
            print("[Client] \"{}\"".format(response))
            resp = utils.send_message(sock, response)
            print("[Server] \"{}\"".format(resp))
            # Wait for a response and disconnect.
        except Exception as e:
            print(e)
            print("Closing...")
            sock.close()
            break

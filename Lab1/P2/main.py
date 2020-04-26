import socket

# We connect to a (host,port) tuple
import utils

ADDRESS_A = ("cc5312.xor.cl", 5312)
ADDRESS_B = ("cc5312.xor.cl", 5313)
sock_A = utils.create_socket(ADDRESS_A)
sock_B = utils.create_socket(ADDRESS_B)

def senAResendB(message):
    resp_A = utils.send_message(sock_A, message)
    resp_B = utils.send_message(sock_B, resp_A)
    return resp_B

# CONNECTION_ADDR = ("cc5312.xor.cl", 5313)

if __name__ == "__main__":
    # sock = utils.create_socket(CONNECTION_ADDR)
    while True:
        try:

            # Read a message from standard input
            response = input("send a message: ")
            # You need to use encode() method to send a string as bytes.
            print("[Client] \"{}\"".format(response))
            # resp = utils.send_message(sock, response)
            resp = senAResendB(response)
            print("[Server] \"{}\"".format(resp))
            # Wait for a response and disconnect.
        except Exception as e:
            print(e)
            print("Closing...")
            sock.close()
            break

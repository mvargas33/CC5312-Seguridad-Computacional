import socket

# We connect to a (host,port) tuple
import utils
import time

ADDRESS_A = ("cc5312.xor.cl", 5312)
ADDRESS_B = ("cc5312.xor.cl", 5313)
sock_A_input, sock_A_output= utils.create_socket(ADDRESS_A)
sock_B_input, sock_B_output = utils.create_socket(ADDRESS_B)

def senAResendB(message):
    """
    Enía message a A, y respues de A la envía a B.
    Retorna Respuesta de B.
    """
    resp_A = utils.send_message(sock_A_input, sock_A_output, message)
    resp_B = utils.send_message(sock_B_input, sock_B_output, resp_A)
    # if not (resp_B == message):
    #     print(resp_B)
    return resp_B, len(resp_A)

def calcBlockSize():
    """
    Retorna el número en bytes del tamaño del bloque.
    Envía mensajes cada vez más largos al servidor (aumentados en 8 bits)
    Y cuenta cada cuantos mensajes enviados, la respuesta del servidor es más larga.
    Es decir, cuantos bytes tuve que agregar para que la respuesta fuera más larga.
    En encriptación por bloques, cuando el texto plano no cabe un bloque del cipher
    se debe agregar otro bloque más. Estamos calculando ese aumento de bytes que corresponde
    justamente al tamaño del bloque. Además se envía la respuesta del servidor A,
    al servidor B para saber la correctitud de la respuesta de A, ya que desde cierto tamaño de mensaje,
    (64 bytes) los mensajes ya no son correctos 
    """
    N = 2**32
    actual = 1
    msg = "a"
    chr_aumentados_para_cambio = []
    rB, largoA = senAResendB(msg)
    largo_anterior = largoA
    msg = "aa"
    counter = 0
    while(actual < N):
        #time.sleep(0.01) # No sobrecargar al servidor
        rB, largoA = senAResendB(msg)
        if(rB == msg): # Correctitud
            if(largoA > largo_anterior):
                chr_aumentados_para_cambio.append(counter + 1)
                counter = 0
                largo_anterior = largoA
            else:
                counter += 1

            # print("coorectitud: " + str(rB == msg) +" message: " + str(len(msg)) + " len(A): " + str(largoA))
            msg += "a"
            actual += 1
        else:
            break
    mas_repetido = max(set(chr_aumentados_para_cambio), key = chr_aumentados_para_cambio.count) # rescata el que tiene más frecuencia
    print(mas_repetido)
    return mas_repetido

if __name__ == "__main__":
    # sock = utils.create_socket(CONNECTION_ADDR)
    while True:
        try:
            calcBlockSize()
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
            sock_A.close()
            sock_B.close()
            break

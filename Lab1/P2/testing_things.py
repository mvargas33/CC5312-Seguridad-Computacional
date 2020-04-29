import socket
from pprint import pprint

# We connect to a (host,port) tuple
import utils
import time

ADDRESS_A = ("cc5312.xor.cl", 5312)
ADDRESS_B = ("cc5312.xor.cl", 5313)
sock_A = utils.create_socket(ADDRESS_A)
sock_B = utils.create_socket(ADDRESS_B)

def senAResendB(message):
    """
    Enía message a A, y respues de A la envía a B.
    Retorna Respuesta de B.
    """
    resp_A = utils.send_message(sock_A, message)
    resp_B = utils.send_message(sock_B, resp_A)
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

# TODO : XOR's ZONE
# Receives ciphered text and block_size
def decode_last_char(c_text, block_size):
    d = {}
    # Get cyphered text as an bytearray
    blocks_array = utils.split_blocks(c_text, block_size)
    # Define block_size
    block_size_arr = len(blocks_array)
    # Get last block or C_{n}
    c_n = blocks_array[len(blocks_array)-1]
    # Get block C_{n-1}
    c_n1 = blocks_array[len(blocks_array)-2]
    # TODO : Error mssg, can be captured, not just hardcoded by a
    # function called experiments of something like that
    error_mssg = "pkcs7: invalid padding (last byte is larger than total length)"
    # C_{n-1}[BlockSize-1] = 0
    c_n1[len(c_n1)-1] = 0
    # Declare M_{n-1}
    m_n1 = c_n1
    blocks_array[len(blocks_array)-2] = m_n1
    # Joinblocks and then cast to hex
    modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
    i = 1
    # Do-While
    while True:
        # Send to sock_B
        resp = utils.send_message(sock_B, modified_c_text)
        # Dictionary
        d[i] = resp
        # Check if there is not a padding error
        #if not resp.startswith('pkcs7'):
        #    break
        # Increase M_{n-1}[BlockSize-1] in one
        m_n1[len(c_n1)-1] = i
        # Create a new M_{n-1}
        blocks_array[len(blocks_array)-2] = m_n1
        # Joinblocks and then cast to hex
        modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
        i+=1
        if i>255:
            break
    # Print dictionary
    pprint(d)
    print("Pasa While")
    print(i)
    # Asegurar que texto plano termina en 0x01
    # Almacenar valor anterior, por si no se asegura
    ant = m_n1[len(c_n1)-2]
    # Cambiar a otro valor
    m_n1[len(c_n1)-1] += 1
    blocks_array[len(blocks_array)-2] = m_n1
    # Joinblocks and then cast to hex
    modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
    # Ask if it still works
    resp = utils.send_message(sock_B, modified_c_text)
    # There is an error message, go back
    if resp.startswith('pkcs7'):
        print("No termina en 0x01")
    m_n1[len(c_n1)-1] = ant
    blocks_array[len(blocks_array)-2] = m_n1
    modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
    # Else there is not, continue with the same M_{n-1}
    print("This code has done something until this point")
    # XOR_1
    # Get M_{n-1}[BlockSize-1]
    value_1 = m_n1[len(m_n1)-1]
    #value_1 = i
    # Get 0x01
    value_2 = 1
    # Do XOR and get I_{n}[Blocksize-1]
    i_n = value_1^value_2

    # XOR_2
    # Get clean c_{n-1}
    blocks_array = utils.split_blocks(c_text, block_size)
    c_n1 = blocks_array[len(blocks_array)-2]
    # Get last byte of c_n1
    value_1 = c_n1[len(c_n1)-1]
    # Recover I_{n}[Blocksize-1]
    value_2 = i_n
    # Do XOR and get B_{n}[BlockSize-1]
    result = value_1^value_2
    print(result)
    return result


if __name__ == "__main__":
    # sock = utils.create_socket(CONNECTION_ADDR)
    # Call block_size here because of strange issue that happened
    block_size = calcBlockSize()
    while True:
        try:
            # Read a message from standard input
            response = input("send a message: ")
            # The next line is a good hint
            # You need to use encode() method to send a string as bytes.
            print("[Client] \"{}\"".format(response))
            print(utils.bytes_to_hex(response.encode()))
            # resp = utils.send_message(sock, response)
            resp_A = utils.send_message(sock_A, response)
            resp_B = utils.send_message(sock_B, resp_A)
            print("[Server] \"{}\"".format(resp_A))
            decode_last_char(resp_A.encode(), block_size)
            # Wait for a response and disconnect.
        except Exception as e:
            print(e)
            print("Closing...")
            sock_A.close()
            sock_B.close()
            break

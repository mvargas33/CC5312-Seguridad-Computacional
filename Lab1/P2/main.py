import socket

# We connect to a (host,port) tuple
import utils
import time
import binascii

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
    i = 0
    rB, largoA = senAResendB(msg)
    i = 1
    largo_anterior = largoA
    msg = "aa"
    counter = 0
    while(actual < N):
        #time.sleep(0.01) # No sobrecargar al servidor
        rB, largoA = senAResendB(msg)
        i+=1
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
    print(i)
    return mas_repetido


def decode_last_char(c_text, block_size):
    """
    Toma un texto cifrado, y tamaño de bloque
    Retorna el último byte del mensaje original del texto cifrado
    :param c_text: byte-like message
    """
    error_mssg = "pkcs7: invalid padding (last byte is larger than total length)" # TODO: Find a way to capture error message for invalid padding
    blocks_array = utils.split_blocks(c_text, block_size)   # Get cyphered text as an bytearray
    n = len(blocks_array)                                   # Cantidad n de bloques
    b = block_size//8                                       # Cantidad b de bytes por bloque

                                                            # Obtener C[n]
    c_n = bytearray(b)                                      # Crea bytearray de largo 128//8 = 16 bytes
    for i in range(0, b - 1):                               # Copia del byte 0 al 15
        c_n[i] = blocks_array[n-1][i]                       # El último bloque
    print("C[n] =   " + str(binascii.hexlify(c_n)))
                                                            # Obtener C[n-1]
    c_n1 = bytearray(b)                                     # Crea bytearray de largo 128//8 = 16 bytes
    for i in range(0, b - 1):                               # Copia del byte 0 al 15
        c_n1[i] = blocks_array[n-2][i]                      # El penúltimo bloque
    print("C[n-1] = " + str(binascii.hexlify(c_n1)))
                                                            # Obtener M[n-1] copiando de C[n-1]
    m_n1 = bytearray(b)                                     # Crea bytearray de largo 128//8 = 16 bytes
    for i in range(0, b - 1):                               # Copia del byte 0 al 15
        m_n1[i] = c_n1[i]                                   # C[n-1]
    print("M[n-1] = " + str(binascii.hexlify(m_n1)))

    i = 0                                                   # De 0 a 256
    while True:
        m_n1[b-1] = i                                       # M[n-1][BlockSize-1] = i
        blocks_array[n-2] = m_n1                            # Sobrescribimos el blocks_Array[n-2] por el M[n-1]
        modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array)) # Joinblocks and then cast to hex
        print(c_text.hex())
        print("\n")
        print(modified_c_text)
        #print("M[n-1] = " + str(binascii.hexlify(blocks_array[n-2])))

        resp = utils.send_message(sock_B_input, sock_B_output, modified_c_text) # Send to sock_B
        if resp != error_mssg:                              # Check if there is not a padding error
            break
        i+=1                                                # Try next i
        if(i == 255):
            print("Se han probado los 256 valores de padding sin éxito")
            exit(1)

    print("Pasa While")
    # Asegurar que texto plano termina en 0x01
    # Almacenar valor anterior, por si no se asegura
    # ant = m_n1[len(c_n1)-2]
    # # Cambiar a otro valor
    # m_n1[len(c_n1)-1] = 42
    # blocks_array[n-2] = m_n1
    # # Joinblocks and then cast to hex
    # modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
    # # Ask if it still works
    # resp = utils.send_message(sock_B_input, sock_B_output, modified_c_text)
    # # There is an error message, go back
    # if resp == error_mssg:
    #     print("No termina en 0x01")
    #     m_n1[len(c_n1)-1] = ant
    #     blocks_array[n-2] = m_n1
    #     modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
    # # Else there is not, continue with the same M_{n-1}
    # print("This code has done something until this point")
    
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
    c_n1 = blocks_array[n-2]
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
    # block_size = calcBlockSize()
    block_size = 16*8
    while True:
        try:
            # Read a message from standard input
            response = input("send a message: ")
            # The next line is a good hint
            # You need to use encode() method to send a string as bytes.
            print("[Client] \"{}\"".format(response))
            # resp = utils.send_message(sock, response)
            resp = utils.send_message(sock_A_input, sock_A_output, response)
            b = decode_last_char(resp.encode(), block_size)
            print("[Server] \"{}\"".format(resp))
            # Wait for a response and disconnect.
        except Exception as e:
            print(e)
            print("Closing...")
            sock_A_input.close()
            sock_A_output.close()
            sock_B_input.close()
            sock_B_output.close()
            break

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
    error_mssg = "pkcs7: invalid padding"                   # Prefijo de error típico de padding
    blocks_array = utils.split_blocks(c_text, block_size//8)# Get cyphered text as an bytearray
    n = len(blocks_array)                                   # Cantidad n de bloques
    b = block_size//8                                       # Cantidad b de bytes por bloque

    m_n1 = bytearray(b)                                     # Crea bytearray de largo 128//8 = 16 bytes
    for i in range(0, b - 1):                               # Copia del byte 0 al 15
        m_n1[i] = blocks_array[n-2][i]                      # Obtener M[n-1] copiando de C[n-1]

    i = 0                                                   # De 0 a 256
    while True:
        m_n1[b-1] = i                                       # M[n-1][BlockSize-1] = i
        blocks_array[n-2] = m_n1                            # Sobrescribimos el blocks_Array[n-2] por el M[n-1]
        modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array)) # Joinblocks and then cast to hex
        resp = utils.send_message(sock_B_input, sock_B_output, modified_c_text) # Send to sock_B
        if not resp.startswith(error_mssg):                 # Check if there is not a padding error, we have a candidate
                                                            # Validar: Asegurar que texto plano termina en 0x01
            ant = m_n1[b-2]                                 # M[n-1][b-2] penúltimo valor antiguo
            m_n1[b-2] = ant+1 % 256                         # Cambiar a otro valor
            blocks_array[n-2] = m_n1                        # Modificamos M[n-2]
            modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))   # Joinblocks and then cast to hex
            resp = utils.send_message(sock_B_input, sock_B_output, modified_c_text) # Acá tenemos que el texto descifrado es del estilo [.....[0xfe][0x01]]

            if resp == error_mssg:                          # Si no validó estamos en un caso donde podríamos haber encontrado un falso positivo, ej: que el último byte descifrado fuera [0x02] y el byte anterior cifrado [0x02]. Ahora da [...[0xfe][0x02]] y no pasa
                print("No valida, valor encontrado para M[n-1][b-1] incosistente, buscando otro valor ...")
                m_n1[b-2] = ant                             # Always Revert al valor C[n-1][b-2] original
                blocks_array[n-2] = m_n1
                modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
            else:
                m_n1[b-2] = ant                             # Always Revert
                blocks_array[n-2] = m_n1
                modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
                break                                       # Pasó validación, encontramos M[n-1][b-1]
        i+=1
        if(i == 256):
            print("Se han probado los 256 valores de padding sin éxito")
            exit(1)
    
    i_n = i^1 # XOR para obtener I_[n][b-1]. i = M[n-1][b-1], 1 = 0x01
    c_n1_b1 = utils.split_blocks(c_text, block_size//8)[n-2][b-1] # Get clean C[n-2][b-1]
    return i_n, i_n^c_n1_b1 # XOR para obtener B_[n][b-1]

def decode_last_block2(c_text, block_size, i_n_b1):
    """
    Toma un texto cifrado, y tamaño de bloque
    Retorna el último bloque del mensaje original del texto cifrado
    :param c_text: byte-like message
    """
    error_mssg = "pkcs7: invalid padding"                       # Prefijo de error típico de padding
    blocks_array = utils.split_blocks(c_text, block_size//8)    # Get cyphered text as an bytearray
    n = len(blocks_array)                                       # Cantidad n de bloques
    b = block_size//8                                           # Cantidad b de bytes por bloque

    i_n = bytearray(b)                                          # Crea bytearray de largo 128//8 = 16 bytes
    for i in range(0, b - 2):                                   # Copia del byte 0 al 15
        i_n[i] = 0
    i_n[b-1] = i_n_b1                                           # Único Valor conocido a la fecha

    queremos = b - 2                                            # Queremos conocer b - 2 al inicio
    while queremos >= 0:
        print("Vamos en el byte: " + str(queremos))
        conocemos = queremos + 1                                # Conocemos de b-1 : b-1, 
        paddingByte = b - queremos                              # Padding byte

        m_n1 = bytearray(b)                                     # Crea bytearray de largo 128//8 = 16 bytes
        for i in range(0, b):                                   # [[0].....................[b-1]]
            m_n1[i] = blocks_array[n-2][i]                      # M[n-1] = C[n-1]

        for i in range(conocemos, b):                           # [.........[conocemos]....[b-1]]
            m_n1[i] = i_n[i]^paddingByte                        # M[n-1] = I[n] XOR PaddingByte, para que al hacer el servidor M[n-1][i] XOR I[n-1][i] de PaddingByte
        
        i = 0                                                   # De 0 a 256
        while True:
            m_n1[queremos] = i                                  # M[n-1][Queremos] = i
            blocks_array[n-2] = m_n1                            # Sobrescribimos el blocks_Array[n-2] por el M[n-1]
            modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array)) # Joinblocks and then cast to hex
            resp = utils.send_message(sock_B_input, sock_B_output, modified_c_text) # Send to sock_B
            if not resp.startswith(error_mssg):                 # Check if there is not a padding error, we have a candidate
                if queremos != 0:                               # Si el es primer byte, no podemos validar
                    
                    # Validar: Asegurar que texto plano termina en 0x01
                    ant = m_n1[queremos-1]                      # M[n-1][queremos-1] penúltimo valor antiguo
                    m_n1[queremos-1] = ant+1 % 256              # Cambiar a otro valor
                    blocks_array[n-2] = m_n1                    # Modificamos M[n-2]
                    modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))   # Joinblocks and then cast to hex
                    resp = utils.send_message(sock_B_input, sock_B_output, modified_c_text) # Ask if it still works

                    if resp.startswith(error_mssg):             # No validó There is an error message, go back
                        print("No valida, valor encontrado para M[n-1][queremos] incosistente, buscando otro valor ...")
                        m_n1[queremos-1] = ant                  # Always Revert
                        blocks_array[n-2] = m_n1
                        modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
                    else:
                        m_n1[queremos-1] = ant                  # Always Revert
                        blocks_array[n-2] = m_n1
                        modified_c_text = utils.bytes_to_hex(utils.join_blocks(blocks_array))
                        break                                   # Pasó validación, encontramos M[n-1][queremos]
                else:
                    break
            i+=1                                                # Try next i
            if(i == 256):
                print("Se han probado los 256 valores de padding sin éxito")
                exit(1)
                
        i_n[queremos] = i^paddingByte # XOR para obtener I_[n][queremos]. i = M[n-1][queremos], paddingByte = 0x02, 0x03 ...
        queremos -= 1

    # Obtener el último bloque
    c_n1 = utils.split_blocks(c_text, block_size//8)[n-2]       # Get clean C[n-2][b-1]
    b_n = bytearray(b)                                          # Crea bytearray de largo 128//8 = 16 bytes
    for i in range(0, b):                                   # Copia del byte 0 al 15
        b_n[i] = i_n[i]^c_n1[i]
    print(b_n)
    #print(binascii.unhexlify(b_n.hex()))
    return b_n                                                  # Return bytearray del texto descifrado


def decode_all_blocks2(c_text, block_size):
    """
    Dado un texto cifrado y tamaño de bloque,
    Retorna el texto plano del texto cifrado
    :param c_text: byte-like array
    """
    blocks_array = utils.split_blocks(c_text, block_size//8)    # Get cyphered text as an bytearray
    n = len(blocks_array)                                       # Cantidad n de bloques
    plain_text = []

    for i in range(n-1, 0, -1):
        print("Vamos en el bloque: " + str(i+1) + "/" + str(n))
        modified_c_text = utils.join_blocks(blocks_array[0:i+1])      # Ya es byte-like

        print("Vamos en el byte: " + str(block_size//8 - 1))
        i_n_b1, b = decode_last_char(modified_c_text, block_size)   # Ya es byte-like
        plain_text.append(decode_last_block2(modified_c_text, block_size, i_n_b1))

    print('')
    for i in range(len(plain_text)-1, 0 - 1, -1):
        print(plain_text[i])
    #print(plain_text)
    #print(binascii.unhexlify(utils.bytes_to_hex(plain_text)))
    return plain_text


if __name__ == "__main__":
    # sock = utils.create_socket(CONNECTION_ADDR)
    # Call block_size here because of strange issue that happened
    # block_size = calcBlockSize()
    
    block_size = 16*8
    while True:
        try:
            
            response = input("send a message: ") # Read a message from standard input
            print("[Client] Plaintext:  \"{}\"".format(response))

            resp = utils.send_message(sock_A_input, sock_A_output, response)
            decode_all_blocks2(utils.hex_to_bytes(resp), block_size)

            #i_n_b1, b = decode_last_char(resp.encode(), block_size)
            #decode_last_block2(resp.encode(), block_size, i_n_b1)

            print('')
            print("[Server] Ciphertext: \"{}\"".format(resp))
        except Exception as e:
            print(e)
            print("Closing...")
            sock_A_input.close()
            sock_A_output.close()
            sock_B_input.close()
            sock_B_output.close()
            break

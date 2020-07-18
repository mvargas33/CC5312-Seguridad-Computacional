from memcached import Memcached
from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.ntp import NTPPrivate
from scapy.layers.dns import DNS, DNSQR

import sys
# https://stackoverflow.com/questions/11914472/stringio-in-python3
from io import StringIO
from scapy.layers import inet
from scapy.all import *

# ==============================================================================
# Memcached Stats
memcached_stats=f'stats\r\n'
# ==============================================================================

# Memcached Stats_Settings
memcached_stats_settings = f'stats settings\r\n'

# ==============================================================================
# Memcached Set
key = "a"
flag = 0
exptime = 3600
text = "a"*1430 # se cae con 1460
amount_of_bytes = len(text)
memcached_set=f'set {key} {flag} {exptime} {amount_of_bytes}\n{text}\r\n'
# ==============================================================================

# ==============================================================================
# Memcached Get
key = "a"
memcached_get=f'get {key}\r\n'
# ==============================================================================

# Memcached Set (corrected)
key = b'a'*1400
command = 'set %s 0 %d %d\r\n%s\r\n' % ('a', 0, len(key), key)

def send_memcached(ip, port):
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

    #ans.show()


def send_dns(ip, port):
    print(f"dns: {ip}:{port}")
    pkt = IP(dst=ip) / UDP(sport=54323, dport=port) / DNS(rd=1, id=12345,  qd=DNSQR(
        qtype=16, qname="lab4.cc5312.xor.cl"))  # qtype=1 is A and DNS Request ID is 12345
    
    # Captura de lo enviado
    capture_1 = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture_1
    pkt.show()
    sys.stdout = save_stdout
    print("len enviado:" + str(len(capture_1.getvalue())))

    print(f"Sending: {pkt.summary()}")
    # ANS is like  IP(src=ip, dst=<myip>) / UDP(sport=port, dport=54323) / DNS(rd=1, qd=DNSQR(qtype=1, qname="lab4.cc5312.xor.cl") an=[<RRs received>]) # 1 is A
    
    ans = sr1(pkt, verbose=1)
    print(f"received:")

    # Captura de la respuesta
    capture = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture
    ans.show()
    sys.stdout = save_stdout 
    print(f'RECEIVED LEN :{len(capture.getvalue())}\n')
    
    quotient = len(capture.getvalue())/len(capture_1.getvalue())
    print(quotient)
    #ans.show()


def send_ntp(ip, port):
    print(f"ntp: {ip}:{port}")
    pkt = IP(dst=ip) / UDP(sport=54322, dport=port) / NTPPrivate(version=3,
                                                                 mode=7, implementation=3, request_code=42)  # 42 is mon_getlist_1
    print(f"Sending: {pkt.summary()}")
    ans = sr1(pkt, verbose=1)
    print(f"received:")
    ans.show()


TEST_IP = "172.17.69.106"

DNS_PORT = 53
NTP_PORT = 123
MEMCACHED_PORT = 11211

if __name__ == "__main__":
    #send_memcached(TEST_IP, MEMCACHED_PORT)
    send_dns(TEST_IP, DNS_PORT)
    #send_ntp(TEST_IP, NTP_PORT)

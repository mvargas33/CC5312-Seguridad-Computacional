import logging
logger = logging.getLogger("scapy")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

from scapy.all import *
from scapy.layers.inet import UDP


# UDP Header from https://github.com/memcached/memcached/blob/master/doc/protocol.txt
class Memcached(Packet):
    name = "Memcached"
    fields_desc = [ ShortField("reqid", 0),
                    ShortField("seqn", 0),
                    ShortField("datagrams", 1),
                    ShortField("reserved", 0), 
                    StrField("msg", "\r\n", fmt="s")]


# Telling scapy that an UDP package could contain a Memcached payload
bind_layers( UDP, Memcached, sport=11211 )
bind_layers( UDP, Memcached, dport=11211 )
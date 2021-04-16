import queue

# General
VERSION_MAJOR = 0
VERSION_MINOR = 1


# this class holds a bunch a queues which is used by HIStack
class LayerQueues:
    q_to_eth_from_int = None      # queue from which ethernet reads and in which interface puts frames
    q_to_int_from_eth = None      # queue to which ethernet sends and from which interface gets frames
    q_to_eth_from_ipv4 = None
    q_to_eth_from_arp = None
    q_to_arp_from_eth = None
    q_to_ipv4_from_eth = None
    q_to_tcp_from_ip = None
    q_to_ip_from_tcp = None
    q_to_udp_from_ip = None
    q_to_ip_from_udp = None
    q_to_icmp_from_ip = None
    q_to_ip_from_icmp = None

    def __init__(self):
        self.q_to_eth_from_int = queue.SimpleQueue()
        self.q_to_int_from_eth = queue.SimpleQueue()
        self.q_to_eth_from_ipv4 = queue.SimpleQueue()
        self.q_to_eth_from_arp = queue.SimpleQueue()
        self.q_to_arp_from_eth = queue.SimpleQueue()
        self.q_to_ipv4_from_eth = queue.SimpleQueue()
        self.q_to_tcp_from_ip = queue.SimpleQueue()
        self.q_to_ip_from_tcp = queue.SimpleQueue()
        self.q_to_udp_from_ip = queue.SimpleQueue()
        self.q_to_ip_from_udp = queue.SimpleQueue()
        self.q_to_icmp_from_ip = queue.SimpleQueue()
        self.q_to_ip_from_icmp = queue.SimpleQueue()


# Interface
ETH_P_ALL = 3               # capture type to capture all the packets
MAX_PKT_SIZE = 4096         # max packet size, should be a power of 2
DEFAULT_INTERFACE = 'dum0'  # default interface name
INTERFACE_MAX_LEN = 24      # maximum length of the interface name

# Ethernet


class MacAddress:
    addr = bytearray(6)

    def __init__(self, address: bytes):
        self.__addr = address

    def __hash__(self):
        return hash((self.__addr,))

    def __eq__(self, other):
        return (self.__addr) == (other.__addr)

    def __ne__(self, other):
        return not(self == other)

    def to_string(self):
        pass

    @staticmethod
    def from_string(address: str):
        pass


DEFAULT_MTU = 1500
DEFAULT_MAC = MacAddress(bytes([0x1A, 0x2B, 0x3C, 0x4D, 0x5E, 0x6F]))
MAC_BROADCAST = MacAddress(bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]))
ETHERTYPE_IPV4 = 0x0800
ETHERTYPE_ARP = 0x0806
ETHERTYPE_IPV6 = 0x86DD
ETHERTYPE_WOL = 0x0842


# ARP

ARP_OP_REQUEST = 1
ARP_OP_REPLY = 2
DEFAULT_ARP_CACHE_TIMEOUT = 14400

# IPv4


class IPv4Address:
    addr = bytearray(6)

    def __init__(self, address: bytes):
        self.__addr = address

    def __hash__(self):
        return hash((self.__addr,))

    def __eq__(self, other):
        return (self.__addr) == (other.__addr)

    def __ne__(self, other):
        return not(self == other)

    def to_string(self):
        pass

    @staticmethod
    def from_string(address: str):
        pass


IPV4_BROADCAST = IPv4Address(bytes([255, 255, 255, 255]))

# TCP
DEFAULT_MSS = 1460


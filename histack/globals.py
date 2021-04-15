# General
VERSION_MAJOR = 0
VERSION_MINOR = 1

# Interface
ETH_P_ALL = 3               # capture type to capture all the packets
MAX_PKT_SIZE = 4096         # max packet size, should be a power of 2
DEFAULT_INTERFACE = 'dum0'  # default interface name
INTERFACE_MAX_LEN = 24      # maximum length of the interface name

# Ethernet


class MacAddress:
    __addr = bytearray(6)

    def __init__(self, address: bytes):
        self.__addr = address

    def to_string(self):
        pass

    @staticmethod
    def from_string(address: str):
        pass


DEFAULT_MTU = 1500
DEFAULT_MAC = MacAddress(bytes([0x1A, 0x2B, 0x3C, 0x4D, 0x5E, 0x6F]))
MAC_BROADCAST = MacAddress(bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]))


# IPv4


class IPv4Address:
    __addr = bytearray(6)

    def __init__(self, address: bytes):
        self.__addr = address

    def to_string(self):
        pass

    @staticmethod
    def from_string(address: str):
        pass


IPV4_BROADCAST = IPv4Address(bytes([255, 255, 255, 255]))

# TCP
DEFAULT_MSS = 1460


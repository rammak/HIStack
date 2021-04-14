# General
VERSION_MAJOR = 0
VERSION_MINOR = 1

# Interface
ETH_P_ALL = 3               # capture type to capture all the packets
MAX_PKT_SIZE = 4096         # max packet size, should be a power of 2
DEFAULT_INTERFACE = 'dum0'  # default interface name
INTERFACE_MAX_LEN = 24      # maximum length of the interface name

# Ethernet
DEFAULT_MTU = 1500
DEFAULT_MAC = bytes([0x1A, 0x2B, 0x3C, 0x4D, 0x5E, 0x6F])
MAC_BROADCAST = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

# IPv4
IPV4_BROADCAST = bytes([255, 255, 255, 255])

# TCP
DEFAULT_MSS = 1460

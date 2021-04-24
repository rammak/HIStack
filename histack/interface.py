"""
interface.py

Uses PF_PACKET socket to communicate with the dummy interface.

Author: Rutwij Makwana (rutwij@dal.ca)
"""
import socket
import logging
from histack.globals import *


class Interface:
    name = None
    rx_bytes = 0
    tx_bytes = 0
    rx_packets = 0
    tx_packets = 0
    __raw_socket = None
    __bound = False
    log = None

    def __init__(self, log_level=logging.INFO):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_level)
        pass

    def start(self, interface_name: str = DEFAULT_INTERFACE) -> bool:
        """Initialize the interface and bind a socket to it."""
        if len(interface_name) > INTERFACE_MAX_LEN or interface_name[0].isdigit():
            return False
        self.name = interface_name
        self.log.info(f'Initializing interface {self.name}')
        self.__raw_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        self.__raw_socket.bind((self.name, 0))
        self.__bound = True
        return True

    def receive(self) -> bytes:
        """Receive raw Ethernet frame from the interface in blocking mode."""
        pac = self.__raw_socket.recv(MAX_PKT_SIZE)
        self.rx_bytes += len(pac)
        self.rx_packets += 1
        self.log.debug(f"Received raw frame of size {len(pac)}")
        return pac

    def send(self, data) -> int:
        """Send raw Ethernet frame to the interface. Returns number of bytes sent."""
        self.tx_bytes += len(data)
        self.tx_packets += 1
        self.log.debug(f"Sent raw frame of size {len(data)}")
        return self.__raw_socket.send(data)

    def stop(self):
        """Close socket bound to the interface."""
        self.log.info(f'Stopping interface {self.name}')
        if self.__raw_socket is not None and self.__bound is True:
            self.__raw_socket.close()
            self.__bound = False

    def __del__(self):
        self.log.info(f'Stopping interface {self.name}')
        if self.__raw_socket is not None and self.__bound is True:
            self.__raw_socket.close()

"""
histack.py

Defines HIStack class which is used to initialize a stack

Author: Rutwij Makwana (rutwij@dal.ca)
"""

import threading
import logging
import sys
from histack.globals import *
from histack.interface import Interface
from histack.l2_ethernet import Ethernet
from histack.l2_arp import ARP


class HIStack:
    name: str = None
    interface: Interface = None
    ethernet: Ethernet = None
    arp: ARP = None
    logger: logging.Logger = None
    mac_address: MacAddress = None
    ipv4_address: IPv4Address = None

    __has_interface = False
    __has_ethernet = False
    __has_arp = False
    __has_ipv4 = False
    __has_icmp = False
    __has_udp = False
    __has_tcp = False

    q: LayerQueues = None            # Queues object which holds all the queues

    __thread_inter_rx = None    # this thread receives packets from the interface and put it in __eth_rx_q
    __thread_inter_tx = None    # this thread sends packets from __eth_tx_q and send them through interface

    def __init__(self, name: str, mac_address: MacAddress, ipv4_address: IPv4Address, log_level=logging.DEBUG):
        self.name = name
        self.q = LayerQueues()
        self.mac_address = mac_address
        self.ipv4_address = ipv4_address
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.info("HIStack initialized")

    def __del__(self):
        pass

    def start(self):
        if self.__has_interface is True and self.__has_ethernet is True:
            if self.__thread_inter_tx is None or self.__thread_inter_tx.is_alive() is False:
                self.__thread_inter_tx = threading.Thread(target=self.interface_tx_thread)
                self.__thread_inter_tx.start()
                self.logger.debug("__thread_inter_tx started")

            if self.__thread_inter_rx is None or self.__thread_inter_rx.is_alive() is False:
                self.__thread_inter_rx = threading.Thread(target=self.interface_rx_thread)
                self.__thread_inter_rx.start()
                self.logger.debug("__thread_inter_rx started")

            if self.__has_ethernet is True:
                self.ethernet.start()

        else:
            return False

    def interface_rx_thread(self):
        while True:
            self.q.q_to_eth_from_int.put(self.interface.receive())
            # self.logger.debug("Received a packet")
            # self.logger.debug("Received a packet")

    def interface_tx_thread(self):
        while True:
            self.interface.send(self.q.q_to_int_from_eth.get())
            # self.logger.debug("Sent a packet")
            # self.logger.debug("Sent a packet")

    def register_interface(self, interface_name: str) -> bool:
        self.interface = Interface(log_level=logging.INFO)
        self.__has_interface = self.interface.start(interface_name)
        return self.__has_interface

    def register_arp(self):
        if self.__has_arp is False:
            return False
        self.arp = ARP(mac_address=self.mac_address, ip_address=self.ipv4_address, queues=self.q)
        self.__has_arp = True
        return self.__has_arp

    def register_ethernet(self, mtu: int = DEFAULT_MTU) -> bool:
        if self.__has_interface is False:
            return False
        self.ethernet = Ethernet(mac_address=self.mac_address, arp=self.arp, queues=self.q, mtu=mtu,
                                 log_level=logging.DEBUG)
        self.__has_ethernet = True
        return True

    def register_ipv4(self, ipv4_address: IPv4Address) -> bool:
        pass

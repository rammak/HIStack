"""
histack.py

Defines HIStack class which is used to initialize a stack

Author: Rutwij Makwana (rutwij@dal.ca)
"""

import queue
import threading
import logging
import sys
from histack.globals import *
from histack.interface import Interface


class HIStack:
    name = None
    interface = None
    logger = None

    __has_interface = False
    __has_ethernet = False
    __has_arp = False
    __has_ipv4 = False
    __has_icmp = False
    __has_udp = False
    __has_tcp = False

    __eth_rx_q = None           # queue from which ethernet reads and in which interface puts frames
    __eth_tx_q = None           # queue to which ethernet sends and from which interface gets frames

    __thread_inter_rx = None    # this thread receives packets from the interface and put it in __eth_rx_q
    __thread_inter_tx = None    # this thread sends packets from __eth_tx_q and send them through interface

    def __init__(self, name: str, log_level=logging.DEBUG):
        self.name = name
        # todo: fix logger
        self.logger = logging.getLogger('main_logger')
        self.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        self.logger.setLevel(log_level)
        self.logger.info("HIStack initialized")

    def __del__(self):
        pass

    def start(self):
        print("In start")
        if self.__has_interface is True and self.__has_ethernet is True:
            # print(self.__thread_inter_tx, self.__thread_inter_tx.is_alive())
            if self.__thread_inter_tx is None or self.__thread_inter_tx.is_alive() is False:
                self.__thread_inter_tx = threading.Thread(target=self.interface_tx_thread)
                self.__thread_inter_tx.start()
                self.logger.debug("__thread_inter_tx started")

            if self.__thread_inter_rx is None or self.__thread_inter_rx.is_alive() is False:
                self.__thread_inter_rx = threading.Thread(target=self.interface_rx_thread)
                self.__thread_inter_rx.start()
                self.logger.debug("__thread_inter_rx started")

            return True
        else:
            return False


    def interface_rx_thread(self):
        print("rxrx")
        while True:
            self.__eth_rx_q.put(self.interface.receive())
            # self.logger.debug("Received a packet")
            print("Received a packet")

    def interface_tx_thread(self):
        print("txtx")
        while True:
            self.interface.send(self.__eth_tx_q.get())
            # self.logger.debug("Sent a packet")
            print("Sent a packet")

    def register_interface(self, interface_name: str) -> bool:
        self.interface = Interface()
        self.__has_interface = self.interface.start(interface_name)
        print(self.__has_interface)
        return self.__has_interface

    def register_ethernet(self, mac_address: MacAddress = DEFAULT_MAC, mtu: int = DEFAULT_MTU) -> bool:
        if self.__has_interface is False:
            return False
        self.__eth_rx_q = queue.SimpleQueue()
        self.__eth_tx_q = queue.SimpleQueue()
        self.__has_ethernet = True              # todo: initialize ethernet before this
        return True

    def register_ipv4(self, ipv4_address: IPv4Address) -> bool:
        pass
"""
interface.py

Uses PF_PACKET socket to communicate with the dummy interface.

Author: Rutwij Makwana (rutwij@dal.ca)
"""
import socket
import logging
from HIStack.globals import *


class Interface:
    name = None
    __raw_socket = None
    __bound = False

    def __init__(self):
        pass

    def start(self, interface_name: str = DEFAULT_INTERFACE) -> bool:
        if len(interface_name) > INTERFACE_MAX_LEN or interface_name[0].isdigit():
            logging.error("Invalid interface name")
            return False
        self.name = interface_name
        logging.info(f'Initializing interface {self.name}')
        self.__raw_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        self.__raw_socket.bind((self.name, 0))
        self.__bound = True

    def receive(self):
        return self.__raw_socket.recv(MAX_PKT_SIZE)

    def send(self, data):
        return self.__raw_socket.send(data)

    def stop(self):
        logging.info(f'Stopping interface {self.name}')
        if self.__raw_socket is not None and self.__bound is True:
            self.__raw_socket.close()
            self.__bound = False

    def __del__(self):
        logging.info(f'Stopping interface {self.name}')
        if self.__raw_socket is not None and self.__bound is True:
            self.__raw_socket.close()

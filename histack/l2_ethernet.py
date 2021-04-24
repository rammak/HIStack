import queue
import threading
import logging
from histack.globals import *
from histack.l2_arp import ARP


def type_to_str(ether_type: int):
    if ether_type == ETHERTYPE_IPV4:
        return "IPv4"
    elif ether_type == ETHERTYPE_ARP:
        return "ARP"
    elif ether_type == ETHERTYPE_WOL:
        return "Wake-on-LAN"
    elif ether_type == ETHERTYPE_IPV6:
        return "IPv6"
    else:
        return "Unknown"


class EthernetFrame:
    mac_dst: MacAddress = None
    mac_src: MacAddress = None
    ether_type: bytearray = None
    payload = bytearray()
    length = 0

    def __init__(self):
        pass

    def set(self, mac_dst: bytearray, mac_src: bytearray, payload: bytes, ether_type: bytearray = bytearray(b'\x08\x00')):
        if len(mac_dst) != 6 or len(mac_src) != 6:
            return None
        self.mac_src = MacAddress(mac_src)
        self.mac_dst = MacAddress(mac_dst)
        self.ether_type = ether_type
        self.payload = payload

    def get_raw(self):
        return self.mac_dst.addr + self.mac_src.addr + self.ether_type + self.payload

    # def get(self, data: bytes):
    #     self.mac_dst = data[:6]
    #     self.mac_src = data[6:12]
    #     self.ether_type = (data[12] << 8) + data[13]
    #     self.payload = data[14:]

    def print_header(self):
        print("Dst : ", self.mac_dst.to_string(), "\tSrc : ", self.mac_src, "\tType : ",
              type_to_str(self.ether_type[0] << 8 | self.ether_type[1]))


class Ethernet:
    mac_address: MacAddress = None
    mtu: int = 0
    arp: ARP = None
    log = None

    q: LayerQueues = None

    # this thread receives packets from the interface below and pass it on to upper layers
    __t1_down_to_up: threading.Thread = None
    # this thread receives packets from the upper layers and pass it on to the interface
    __t2_up_to_down: threading.Thread = None

    __t1_running = False
    __t2_running = False

    def __init__(self, mac_address: MacAddress, queues: LayerQueues, arp: ARP, mtu: int = DEFAULT_MTU,
                 log_level=logging.INFO):
        self.mac_address = mac_address
        self.q = queues
        self.mtu = mtu
        self.arp = arp

        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_level)

        self.__t1_down_to_up = threading.Thread(target=self.down_to_up)
        self.__t2_up_to_down = threading.Thread(target=self.up_to_down)

        self.log.info(f'Ethernet interface with MAC:{self.mac_address.to_string()} registered.')

    def down_to_up(self):
        while True:
            # stop the thread if stop signal is received
            if self.__t1_running is False:
                break

            # take a frame from the interface
            frame = self.q.q_to_eth_from_int.get()

            # inspect which protocol is used
            ethertype = (frame[12] << 8) + frame[13]

            self.log.debug(f'Received ETH frame of type:{type_to_str(ether_type=ethertype)}')
            # pass on to the appropriate upper layer
            if ethertype == ETHERTYPE_IPV4:
                self.q.q_to_ipv4_from_eth.put(frame[14:])
            elif ethertype == ETHERTYPE_ARP:
                self.q.q_to_arp_from_eth.put(frame[14:])
            else:
                pass

    def up_to_down(self):
        # stop the thread if stop signal is received
        while True:
            if self.__t2_running is False:
                break

            # check if any IPv4 layer packets are queued
            if self.q.q_to_eth_from_ipv4.empty() is False:
                packet = self.q.q_to_eth_from_ipv4.get()

                # build ethernet header
                frame = EthernetFrame()
                frame.set()

                # pass on to the lower interface


    def start(self):
        if self.__t1_down_to_up.is_alive() is False:
            self.__t1_running = True
            self.__t1_down_to_up.start()
            self.log.info("Thread __t1_down_to_up is running.")
        if self.__t2_up_to_down.is_alive() is False:
            self.__t2_running = True
            self.__t2_up_to_down.start()
            self.log.info("Thread __t2_up_to_down is running.")
        return self.__t1_running & self.__t2_running

    def stop(self):
        if self.__t1_down_to_up.is_alive() is True:
            self.__t1_running = False
            self.__t1_down_to_up.join()
        if self.__t2_up_to_down.is_alive() is True:
            self.__t2_running = False
            self.__t2_up_to_down.join()
        return self.__t1_running & self.__t2_running

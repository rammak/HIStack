import threading
import queue
from histack.globals import *

class ARPPacket:
    htype = bytearray([0x00, 0x01])
    ptype = bytearray([0x08, 0x00])
    hlen = bytearray([0x06])
    plen = bytearray([0x04])
    op = bytearray(2)
    sha: MacAddress = None
    spa: IPv4Address = None
    tha: MacAddress = None
    tpa: IPv4Address = None

    def __init__(self, op: int, sha: MacAddress, spa: IPv4Address, tha: MacAddress, tpa: IPv4Address):
        self.op = bytearray([0x00, op])
        self.sha = sha.addr
        self.spa = spa.addr
        self.tha = tha.addr
        self.tpa = tpa.addr

    def get_raw(self):
        return self.htype + self.ptype + self.hlen + self.plen + self.op + self.sha.addr + self.spa.addr + \
               self.tha.addr + self.tpa.addr


class ARP:

    # this is the main arp table
    # keys are the ip addresses and values are a list of corresponding MAC addresses and ttl
    arp_table = dict()
    cache_timeout: int = 0           # ARP cache timeout (default = 4 hours)
    mac_address: MacAddress = None
    ip_address: IPv4Address = None

    q: LayerQueues = None

    # this thread receives packets from the Ethernet layer
    __t1_receive: threading.Thread = None

    __t1_running: bool = False

    def __init__(self, mac_address: MacAddress, ip_address: IPv4Address,
                 queues: LayerQueues,  cache_timeout: int = DEFAULT_ARP_CACHE_TIMEOUT):
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.cache_timeout = cache_timeout
        self.q = queues
        self.__t1_receive = threading.Thread(target=self.__receive)

        # adding own address to arp table with negative timeout so that it never expires
        self.arp_table[self.ip_address] = [self.mac_address, -1]

    def start(self):
        if self.__t1_receive.is_alive() is False:
            self.__t1_running = True
            self.__t1_receive.start()
        return self.__t1_running

    def stop(self):
        if self.__t1_receive.is_alive() is True:
            self.__t1_running = False
            self.__t1_receive.join()
        return self.__t1_running

    def query(self, ip_address: IPv4Address):
        if ip_address in self.arp_table:
            return self.arp_table[ip_address][0]    # returns only MAC address
        else:
            request = ARPPacket(op=ARP_OP_REPLY, sha=self.mac_address, spa=self.ip_address,
                                tha=MacAddress(bytes([0, 0, 0, 0, 0, 0])), tpa=ip_address)
            self.q.q_to_eth_from_arp.put(request)

    def __receive(self):
        while True:
            # if stop signal is received, stop the thread
            if self.__t1_running is False:
                break

            # check is any packets are in the queue
            if self.q.q_to_arp_from_eth.empty() is False:
                packet = self.q.q_to_arp_from_eth.get()

                # note: we are assuming that the link layer is always Ethernet
                op = packet[6] << 8 | packet[7]
                if op == ARP_OP_REQUEST:
                    # send a reply
                    reply = ARPPacket(op=ARP_OP_REPLY, sha=self.mac_address, spa=self.ip_address,
                                      tha=MacAddress(packet[8:14]), tpa=IPv4Address(packet[14:18]))
                    self.q.q_to_eth_from_arp.put(reply.get_raw())

                if op == ARP_OP_REPLY:
                    # update the ARP table
                    self.arp_table[IPv4Address(packet[14:18])] = [MacAddress(packet[8:14]), self.cache_timeout]





"""
histack - An experimantal TCP/IP stack written in Python

Author: Rutwij Makwana (rutwij@dal.ca)
"""

import threading
import logging
import time
import sys
from histack import *
from histack.interface import Interface


def test_interface(i: Interface):
    while True:
        log.info(i.receive())


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)

log.info(f"HIStack V{VERSION_MAJOR}.{VERSION_MINOR}")

st = HIStack(name="stack1", mac_address=DEFAULT_MAC, ipv4_address=IPv4Address.from_string("192.168.0.33"))
st.register_interface(interface_name='dum0')
st.register_ethernet()
st.start()

while True:
    time.sleep(1)


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
        logger.info(i.receive())


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

logger.info(f"histack V{VERSION_MAJOR}.{VERSION_MINOR}")

st = HIStack(name="stack1")
print(st.register_interface(interface_name='dum0'))
print(st.register_ethernet())
print(st.start())

while True:
    time.sleep(1)


"""
HIStack - An experimantal TCP/IP stack written in Python

Author: Rutwij Makwana (rutwij@dal.ca)
"""

import threading
import logging
from HIStack import *
from HIStack.interface import Interface


def test_interface(i: Interface):
    while True:
        logger.info(i.receive())


logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

logger.info(f"HIStack V{VERSION_MAJOR}.{VERSION_MINOR}")

ifc = Interface()
ifc.start()

t = threading.Thread(target=test_interface, args=(ifc,))
t.start()


import logging
import sys
from histack.globals import *
from histack.histack import HIStack

log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)s | %(name)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)
log.setLevel(logging.DEBUG)

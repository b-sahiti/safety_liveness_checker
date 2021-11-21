import logging
import logging.config

"""
    CRITICAL	50
    ERROR	40
    WARNING	30
    INFO	20
    DEBUG	10
    NOTSET	0
"""


log=logging.getLogger("my-logger")
#logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)
logging.basicConfig(format=' %(message)s',level=logging.INFO)
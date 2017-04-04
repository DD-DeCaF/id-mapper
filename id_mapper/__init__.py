import logging
import sys

logger = logging.getLogger('service-id-mapper')
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.setLevel(logging.DEBUG)

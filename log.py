import logging

LOG_FILENAME = 'server.log'

logging.basicConfig(filename=LOG_FILENAME, filemode='a', format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def logInfo(msg):
    logger.info(msg)
import logging
import coloredlogs

logger = logging.getLogger()
coloredlogs.install(fmt="[%(levelname)s][%(asctime)s][%(name)s]#  %(message)s",level='DEBUG', logger=logger)
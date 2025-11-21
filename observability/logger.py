# logger.py - structured JSON logger
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger('sca_metrics')
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

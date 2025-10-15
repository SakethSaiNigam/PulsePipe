from loguru import logger
import os, sys

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL, enqueue=True, backtrace=False, diagnose=False)

def get_logger(name: str):
    return logger.bind(module=name)

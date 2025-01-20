import logging
import sys
from loguru import logger

from app.support.logger import _logger_filter
from config.logging import settings


def register(app=None):
    level = settings.LOG_LEVEL
    path = settings.LOG_PATH
    retention = settings.LOG_RETENTION

    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(level)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True


    # configure loguru
    logger.configure(handlers=[
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {process.name} | {thread.name} |{trace_msg}| {level: <8} | {name}:{function}:{line} - {message}",
            "filter": _logger_filter
        },
        {
            "sink": path,
            "rotation": "00:00",
            "retention": retention,
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {trace_msg} | {name}:{function}:{line} - {message}",
            "filter": _logger_filter
        },
    ])


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

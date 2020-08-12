import logging

LOGGING = True


def setup_logger(name, level):
    # formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    logger = logging.getLogger(name)

    if not logger.handlers:
        formatter = logging.Formatter(fmt='%(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(handler)

    logger.propagate = False

    return logger


def set_logging(log_bool):
    global LOGGING
    LOGGING = log_bool


def is_logging():
    global LOGGING
    return LOGGING


def debug(logger: logging.Logger, msg):
    if is_logging():
        logger.debug(msg)


def info(logger: logging.Logger, msg):
    if is_logging():
        logger.log(logging.INFO, msg)


def error(logger: logging.Logger, msg):
    logger.error(msg)


def log_title(logger: logging.Logger, msg):
    message = ' {} '.format(msg)
    logger.debug("\n\n----------------------------------------------------")
    logger.debug(message.center(52, '-'))
    logger.debug("----------------------------------------------------")

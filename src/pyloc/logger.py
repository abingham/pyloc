import logging

def init_logger():
    logger = logging.getLogger('pyloc')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(name)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger, ch

logger, handler = init_logger()

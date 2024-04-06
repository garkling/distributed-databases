import logging

DEF_FORMAT = "[%(asctime)s][%(levelname)s] - %(name)s.%(funcName)s -- %(message)s"


def get_logger(name, lvl=logging.INFO, fmt=DEF_FORMAT):
    logger = logging.getLogger(name)
    logger.setLevel(lvl)

    sh = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt=fmt,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger


def get_file_logger(name, filename, **kwargs):
    logger = get_logger(name, **kwargs)
    fh = logging.FileHandler(filename, mode='w')
    formatter = logging.Formatter(
        fmt=kwargs.get('fmt', DEF_FORMAT),
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

import os
import time
from contextlib import ContextDecorator

from logger import get_logger

logger = get_logger('executor', fmt='[%(asctime)s][%(levelname)s] - %(name)s -- %(message)s')


class measure(ContextDecorator):

    def __init__(self, section):
        self.section = section
        self.start = None
        self.end = None
        self.dur_s = None

    def __enter__(self):
        logger.info(f'Start executing `{self.section}` #{os.getpid()}')
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.dur_s = round(self.end - self.start, 4)
        logger.info(f'`{self.section}` #{os.getpid()}: elapsed time - {self.dur_s} s')

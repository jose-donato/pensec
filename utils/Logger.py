# Adapted from https://github.com/jlamma/inv_proj/blob/master/logger.py
import logging
import datetime
from enum import Enum

class Logger(object):
    # call with Logger(__name__)
    def __init__(self, config, logdir, level=logging.DEBUG):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.formatter = logging.Formatter('%(levelname)s: %(message)s')

        self.logdir = logdir
        self.addconfiglog()
        self.addconsolelog()
        self.addruntimelog()
    
    def addruntimelog(self):
        self.runtime_handler = logging.FileHandler(self.logdir + "/debug.txt")
        self.runtime_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.runtime_handler)

    def addconfiglog(self):
        config_handler = logging.FileHandler(self.logdir + "/config.txt")
        self.logger.addHandler(config_handler)
        self.logger.debug(str(self.config))
        self.logger.removeHandler(config_handler)
    
    def addconsolelog(self):
        if self.config.OUTPUT_TO_CONSOLE:
            self.cons_handler = logging.StreamHandler()
            self.cons_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.cons_handler)
    
    def debug(self, message):   self.logger.debug(message)
    def info(self, message):    self.logger.info(message)
    def warning(self, message): self.logger.warning(message)
    def error(self, message):   self.logger.error(message)
    def critical(self, message):self.logger.critical(message)

    def end(self):
        self.logger.removeHandler(self.cons_handler)
        if hasattr(self, "cons_handler"):
            self.logger.removeHandler(self.cons_handler)

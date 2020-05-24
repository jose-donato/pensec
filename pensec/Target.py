import os
from datetime import datetime
from pensec.Config import Config

class Target(object):
    def __init__(self, hostname):
        self.hostname = hostname

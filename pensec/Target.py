import os
from datetime import datetime
from pensec.Config import Config

class Target(object):
    def __init__(self, hostname = "scanme.nmap.org", port=None):
        self.hostname = hostname
        self.port = port
        self.common_ports = [22, 80]
    
    def set_target(self, hostname):
        self.hostname = hostname
    
    def set_port(self, port):
        self.port = port

import os
from datetime import datetime
from pensec.Config import Config

class Target(object):
    def __init__(self, hostname = "scanme.nmap.org", port=None):
        self.hostname = hostname
        self.target_ports = {22, 80}
    
    def set_target(self, hostname):
        self.hostname = hostname
    
    def add_port(self, port):
        self.target_ports.add(port)
    def remove_port(self, port):
        self.target_ports.remove(port)
